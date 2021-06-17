import json
from func import get_warnings, get_report, get_script_from_file


class SqlHelper:
    def __init__(self, mysql):
        self.mysql = mysql

    def create_order(self, data):
        email = data['email']
        password = data['password']
        start = data['start']
        dest = data['dest']
        passengers = data['passengers']
        user_id = self.get_user(email, password)
        if user_id is None:  # no user in DB with such email and password
            return 'No user found in DB. Please check your email and password'
        else:
            vehicle_id = self.get_vehicle(passengers)
            user_id = user_id[0]
            if vehicle_id is None:  # no vehicle in DB available with enough capacity
                order_query = """
                    INSERT INTO orders (user_id, start_loc, destination, status, passengers)
                    VALUES ({}, '{}', '{}', '{}', {});""".format(user_id, start, dest, 'new, no vehicle', passengers)
            else:
                vehicle_id = vehicle_id[0]
                order_query = """
                            INSERT INTO orders (user_id, vehicle_id, start_loc, destination, status, passengers)
                            VALUES ({}, {}, '{}', '{}', '{}', {});
                            """.format(user_id, vehicle_id, start, dest, 'new', passengers)
            self.execute_script(order_query)
            get_orders = 'SELECT * FROM orders'
            return 'Created new order\nCurrent orders:\n' + json.dumps(get_report(self.mysql, get_orders), indent=4)

    def get_user(self, email, password):
        get_user_query = """
            SELECT user_id
            FROM users
            WHERE email LIKE '{}'
            AND password LIKE '{}';""".format(email, password)
        return self.execute_and_fetchone(get_user_query)

    def get_vehicle(self, passengers):
        get_vehicle_query = """
            SELECT vehicles.vehicle_id
            FROM vehicles
            JOIN models ON models.model_id = vehicles.model_id
            WHERE models.capacity >= {}
            AND vehicles.status LIKE 'available';""".format(passengers)
        return self.execute_and_fetchone(get_vehicle_query)

    def execute_and_fetchone(self, query):
        conn = self.mysql.connect()
        get_warnings(conn)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def execute_script(self, script):
        conn = self.mysql.connect()
        get_warnings(conn)
        cursor = conn.cursor()

        if ';' in script:
            queries = script.split(';')[:-1]  # get separate sql queries which are separated in file with semicolon
            for line in queries:
                cursor.execute(line)
                conn.commit()
        else:  # there is only 1 query in file without semicolon
            cursor.execute(script)
            conn.commit()

        cursor.close()
        conn.close()  # close connection
        return

    def get_most_popular_models(self, report_file):
        script = get_script_from_file(report_file)
        results = get_report(self.mysql, script)

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
