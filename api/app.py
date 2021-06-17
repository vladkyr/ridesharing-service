from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask_restful import Api
from flaskext.mysql import MySQL
from flask_pymongo import PyMongo

from mysql_helper import SqlHelper
from mongo_helper import MongoHelper
from migration import MigrationHelper
from func import get_script_from_file

app = Flask(__name__)
CORS(app)
api = Api(app)

# mysql configuration
app.config['MYSQL_DATABASE_HOST'] = 'sql'
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'imse_sql_db'

mysql = MySQL(app)
sql_help = SqlHelper(mysql)
mgr_help = MigrationHelper(mysql)

init_db_file = './sql/init_db.sql'
fill_db_file = './sql/fill_db.sql'
report_file = './sql/report.sql'


# mongo configuration
app.config["MONGO_URI"] = "mongodb://user:password@mongo:27017/imse_mongo_db?authSource=admin"
mongo = PyMongo(app)
mongo_db = mongo.db
mng_help = MongoHelper(mongo_db)


@app.route('/', methods=['GET'])
def default():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET'])
def home():
    return {'message': "You are now on the home page"}


@app.route('/init-db', methods=['GET'])
def initialise_db():
    script = get_script_from_file(init_db_file)
    sql_help.execute_script(script)
    return {'message': "Initialised mysql database"}


@app.route('/fill-db', methods=['GET'])
def fill_db():
    script = get_script_from_file(fill_db_file)
    sql_help.execute_script(script)
    return {'message': "Filled mysql database"}


# book-ride is a main use case
@app.route('/book-ride', methods=['GET', 'POST'])
def book_ride():
    if request.method == 'POST':
        data = request.get_json()
        return {'message': sql_help.create_order(data)}
    else:
        return {'message': "You are trying to book a ride via GET"}


@app.route('/report', methods=['GET'])
def report():
    results = sql_help.get_most_popular_models(report_file)
    return {'report_results': results}


@app.route('/mongo', methods=['GET'])
def mongo():
    orders = mng_help.mongo_test()
    # return {'message': json.dumps([order for order in orders])}
    return {'orders': orders}


@app.route('/migration', methods=['GET'])
def migrate():
    return mgr_help.migrate_data()


@app.route('/mongo/book-ride', methods=['GET'])
def mongo_book_ride():
    return {'message': "You are trying book a ride by creating order in mongo DB"}


@app.route('/mongo/report', methods=['GET'])
def get_mongo_report():
    return {'message': "You are trying to get mongo-report"}


if __name__ == '__main__':
    app.run()
