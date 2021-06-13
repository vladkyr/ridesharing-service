from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import json
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
#from flask_mysql_connector import MySQL

app = Flask(__name__)
CORS(app)
api = Api(app)
'''
app.config['MYSQL_USER'] = 'user'
#app.config['MYSQL_ROOT_PASSWORD'] = 'password'
app.config['MYSQL_PASSWORD'] = 'password'
#app.config['MYSQL_HOST'] = '0.0.0.0'
app.config['MYSQL_DB'] = 'knights'
#app.config['MYSQL_DB'] = 'imse_sql_db'
app.config['MYSQL_HOST'] = 'sql'
'''
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'knights'
app.config['MYSQL_DATABASE_HOST'] = 'sql'
mysql = MySQL(app)
mysql.init_app(app)


@app.route('/', methods=['GET'])
def default():
    return {'message': "You are now on the default page"}


@app.route('/connect')
def index():
    return json.dumps({'favorite_colors': favorite_colors()})


def favorite_colors():
    #conn = mysql.connection
    conn = mysql.get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM favorite_colors')
    for (name, color) in cursor:
        print('name', name)
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    conn.close()    # close connection
    print('results', results)
    return results


@app.route('/home', methods=['GET'])
def home():
    return {'message': "You are now on the home page"}


@app.route('/initdb', methods=['GET'])
def initialise_db():
    f = open('./sql/init.sql', 'r')
    script = f.read()
    f.close()
    #conn = mysql.connection
    conn = mysql.get_db()
    cursor = conn.cursor()
    result = cursor.execute(script)
    print('initdb result', result)
    cursor.close()
    conn.close()  # close connection
    return {'message': "Initialised mysql database"}


@app.route('/filldb', methods=['GET'])
def fill_db():
    conn = mysql.get_db()
    cursor = conn.cursor()
    f = open('./sql/filldb.sql', 'r')
    for line in f:
        cursor.execute(line)
    f.close()
    cursor.close()
    conn.close()  # close connection
    return {'message': "Filled mysql database"}


@app.route('/bookride', methods=['GET'])
def book_ride():
    return {'message': "You are trying to book a ride"}


if __name__ == '__main__':
    app.run()
