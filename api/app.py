from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_restful import Api
import json
from flaskext.mysql import MySQL

app = Flask(__name__)
CORS(app)
api = Api(app)

# mysql configuration
app.config['MYSQL_DATABASE_HOST'] = 'sql'
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'knights'
#app.config['MYSQL_DATABASE_DB'] = 'imse_sql_db'
mysql = MySQL(app)
mysql.init_app(app)

'''
init_db_file = './sql/init_db.sql'
fill_db_file = './sql/fill_db.sql'
report_file = './sql/report.sql'
'''
init_db_file = './sql/init_test.sql'
fill_db_file = './sql/fill_test.sql'
report_file = './sql/report_test.sql'



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
@app.route('/book-ride', methods=['GET'])
def book_ride():
    return {'message': "You are trying to book a ride, but this service is not implemented yet"}


@app.route('/report')
def report():
    script = get_script_from_file(report_file)
    results = get_report(script)
    return json.dumps({'report results': results})


def get_script_from_file(filename):
    f = open(filename, 'r')
    script = f.read()
    f.close()
    return script


def execute_script(script):
    conn = mysql.get_db()
    get_warnings(conn)
    cursor = conn.cursor()

    if ';' in script:
        queries = script.split(';')[:-1]  # get separate sql queries which are separated in file with semicolon
        for line in queries:
            # print('line', line)
            cursor.execute(line)
            conn.commit()
    else:   # there is only 1 query in file without semicolon
        cursor.execute(script)
        conn.commit()

    cursor.close()
    conn.close()  # close connection
    return


def get_report(script):
    conn = mysql.get_db()
    get_warnings(conn)
    cursor = conn.cursor()
    cursor.execute(script)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print('report results:', results)
    return results


def get_warnings(connection):
    warnings = connection.show_warnings()
    if warnings:
        print('warnings:', warnings)


if __name__ == '__main__':
    app.run()
