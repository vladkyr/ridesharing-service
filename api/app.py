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


@app.route('/', methods=['GET'])
def default():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET'])
def home():
    return {'message': "You are now on the home page"}


@app.route('/connect')
def index():
    return json.dumps({'favorite_colors': favorite_colors()})


def favorite_colors():
    conn = mysql.get_db()   # open connection to db
    warnings = conn.show_warnings()
    if warnings:
        print('warnings:', warnings)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM favorite_colors')
    results = cursor.fetchall()
    cursor.close()
    conn.close()    # close connection
    print('results', results)
    return results


@app.route('/initdb', methods=['GET'])
def initialise_db():
    script = get_script_from_file('./sql/init_db.sql')
    execute_script(script)
    return {'message': "Initialised mysql database"}


@app.route('/filldb', methods=['GET'])
def fill_db():
    script = get_script_from_file('./sql/fill_db.sql')
    execute_script(script)
    return {'message': "Filled mysql database"}


def get_script_from_file(filename):
    f = open(filename, 'r')
    script = f.read()
    f.close()
    return script


def execute_script(script):
    conn = mysql.get_db()
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


@app.route('/book-ride', methods=['GET'])
def book_ride():
    return {'message': "You are trying to book a ride"}


if __name__ == '__main__':
    app.run()
