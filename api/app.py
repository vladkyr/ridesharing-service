from flask import Flask, request
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

init_db_file = './sql/init_db.sql'
fill_db_file = './sql/fill_db.sql'
report_file = './sql/report.sql'


# mongo configuration
app.config["MONGO_URI"] = "mongodb://user:password@mongo:27017/imse_mongo_db?authSource=admin"
mongo = PyMongo(app)
mongo_db = mongo.db
mng_help = MongoHelper(mongo_db)

mgr_help = MigrationHelper(mysql, mongo_db)


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


@app.route('/migrate', methods=['GET'])
def migrate():
    return mgr_help.migrate_data()


@app.route('/mongo/book-ride', methods=['GET', 'POST'])
def mongo_book_ride():
    if request.method == 'POST':
        data = request.get_json()
        return {'message': mng_help.create_order(data)}
    else:
        return {'message': "You are trying to book a ride in MongoDB via GET"}


@app.route('/mongo/report', methods=['GET'])
def mongo_report():
    results = mng_help.get_most_popular_models()
    return {'report_results': results}


if __name__ == '__main__':
    app.run()
