from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS
from flask_restful import Api
import json
from flaskext.mysql import MySQL
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
api = Api(app)

# mysql configuration
app.config['MYSQL_DATABASE_HOST'] = 'sql'
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'imse_sql_db'

mysql = MySQL(app)
# mysql.init_app(app)

init_db_file = './sql/init_db.sql'
fill_db_file = './sql/fill_db.sql'
report_file = './sql/report.sql'


# mongo configuration
app.config["MONGO_URI"] = "mongodb://user:password@mongo:27017/imse_mongo_db?authSource=admin"
'''app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'imse_mongo_db'
app.config['MONGO_USERNAME'] = 'user'
app.config['MONGO_PASSWORD'] = 'password'
app.config['MONGO_AUTH_SOURCE'] = 'admin'
'''

mongo = PyMongo(app)
# mongo.init_app(app)
mongo_db = mongo.db

# uri = 'mongodb://user:password@mongo:27017/imse_mongo_db'
# mongo = MongoClient(uri)
# mongo_db = mongo.get_database()


@app.route('/', methods=['GET'])
def default():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET'])
def home():
    return {'message': "You are now on the home page"}


@app.route('/init-db', methods=['GET'])
def initialise_db():
    script = get_script_from_file(init_db_file)
    execute_script(script)
    return {'message': "Initialised mysql database"}


@app.route('/fill-db', methods=['GET'])
def fill_db():
    script = get_script_from_file(fill_db_file)
    execute_script(script)
    return {'message': "Filled mysql database"}


# book-ride is a main use case
@app.route('/book-ride', methods=['GET', 'POST'])
def book_ride():
    if request.method == 'POST':
        data = request.get_json()
        return {'message': create_order(data)}
    else:
        return {'message': "You are trying to book a ride via GET"}


@app.route('/report', methods=['GET'])
def report():
    script = get_script_from_file(report_file)
    results = get_report(script)

    results_list = []
    for result in results:
        # avg_trip_time, avg_passengers should be converted to int/str/float) because Decimal is not JSON serializable
        result = {
            'manufacturer': result[0],
            'model': result[1],
            'capacity': result[2],
            'trips': result[3],
            'avg_trip_time': int(result[4]),
            'avg_passengers': round(float(result[5]), 1)
        }
        results_list.append(result)
    return {'report_results': results_list}
    # return {'message': 'successfully produced report', 'report_results': results_list}


@app.route('/mongo', methods=['GET'])
def mongo():
    print('mongo_db', mongo_db)
    print('mongo_db.orders.find()', [result for result in mongo_db.orders.find()])
    mongo_db.orders.insert_one({
        '_id': 12345,
        'user': 'userX',
        'start': 'start1',
        'dest': 'dest1'
    })
    orders = [result for result in mongo_db.orders.find()]
    print('orders', orders)
    # return {'message': json.dumps([order for order in orders])}
    return {'orders': orders}


@app.route('/migrate-data', methods=['GET'])
def migrate_data():
    vehicles = get_vehicle_data()
    users = get_user_data()
    return {'vehicle_data': vehicles, 'user_data': users}
    # return {'message': "You are now on the migrate-data page"}


def get_user_orders(user_id):
    user_orders = '''
        SELECT order_id, vehicle_id, start_loc, destination, status, passengers
        FROM orders
        WHERE user_id = {}; 
    '''.format(user_id)
    orders = get_report(user_orders)
    user_history = '''
        SELECT order_id, vehicle_id, start_loc, destination, passengers, end_time, distance, trip_time, price
        FROM history_orders
        WHERE user_id = {}; 
    '''.format(user_id)
    hist_orders = get_report(user_history)
    print('orders type', type(orders))
    print('hist_orders type', type(hist_orders))
    return orders, hist_orders


def get_user_data():
    user_data = '''
        SELECT user_id, name, email, password, balance
        FROM users; 
    '''
    users = get_report(user_data)
    return users


def get_vehicle_data():
    vehicle_data = '''
        SELECT vehicle_id, manufacturer, model, capacity, status, number_plate
        FROM vehicles
        JOIN models ON vehicles.model_id = models.model_id; 
    '''
    vehicles = get_report(vehicle_data)
    return vehicles


@app.route('/mongo-book-ride', methods=['GET'])
def mongo_book_ride():
    return {'message': "You are trying book a ride by creating order in mongo DB"}


@app.route('/mongo-report', methods=['GET'])
def get_mongo_report():
    return {'message': "You are trying to get mongo-report"}


def create_order(data):
    email = data['email']
    password = data['password']
    start = data['start']
    dest = data['dest']
    passengers = data['passengers']
    user_id = get_user(email, password)
    if user_id is None:   # no user in DB with such email and password
        return 'No user found in DB. Please check your email and password'
    else:
        vehicle_id = get_vehicle(passengers)
        user_id = user_id[0]
        if vehicle_id is None:  # no vehicle in DB available with enough capacity
            order_query = """
                INSERT INTO orders (user_id, start_loc, destination, status, passengers)
                VALUES ({}, '{}', '{}', '{}', {});""".format(user_id, start, dest, 'new, no vehicle', passengers)
        else:
            vehicle_id = vehicle_id[0]
            order_query = """
                        INSERT INTO orders (user_id, vehicle_id, start_loc, destination, status, passengers)
                        VALUES ({}, {}, '{}', '{}', '{}', {});""".format(user_id, vehicle_id, start, dest, 'new', passengers)
        execute_script(order_query)
        get_orders = 'SELECT * FROM orders'
        return 'Created new order\nCurrent orders:\n' + json.dumps(get_report(get_orders), indent=4)


def get_user(email, password):
    get_user_query = """
        SELECT user_id
        FROM users
        WHERE email LIKE '{}'
        AND password LIKE '{}';""".format(email, password)
    return execute_and_fetchone(get_user_query)


def get_vehicle(passengers):
    get_vehicle_query = """
        SELECT vehicles.vehicle_id
        FROM vehicles
        JOIN models ON models.model_id = vehicles.model_id
        WHERE models.capacity >= {}
        AND vehicles.status LIKE 'available';""".format(passengers)
    return execute_and_fetchone(get_vehicle_query)


def execute_and_fetchone(query):
    conn = mysql.connect()
    get_warnings(conn)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def get_script_from_file(filename):
    f = open(filename, 'r')
    script = f.read()
    f.close()
    return script


def execute_script(script):
    conn = mysql.connect()
    get_warnings(conn)
    cursor = conn.cursor()

    if ';' in script:
        queries = script.split(';')[:-1]  # get separate sql queries which are separated in file with semicolon
        for line in queries:
            cursor.execute(line)
            conn.commit()
    else:   # there is only 1 query in file without semicolon
        cursor.execute(script)
        conn.commit()

    cursor.close()
    conn.close()  # close connection
    return


def get_report(script):
    conn = mysql.connect()
    get_warnings(conn)
    cursor = conn.cursor()
    cursor.execute(script)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    # print('report results:', results)
    return results


def get_warnings(connection):
    warnings = connection.show_warnings()
    if warnings:
        print('warnings:', warnings)


if __name__ == '__main__':
    app.run()
