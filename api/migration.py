import json
from func import get_report


class MigrationHelper:
    def __init__(self, mysql, mongo_db):
        self.mysql = mysql
        self.mongo_db = mongo_db

    def migrate_data(self):
        self.migrate_vehicle_data()
        self.migrate_user_data()
        # mongo_vehicle_data = self.migrate_vehicle_data()
        # mongo_user_data = self.migrate_user_data()
        # return {'mongo_vehicle_data': mongo_vehicle_data, 'mongo_user_data': mongo_user_data}
        return {'message': "Data successfully migrated from Mysql to Mongo"}

    def migrate_vehicle_data(self):
        vehicles = self.get_vehicle_data()
        self.mongo_db.vehicles.insert_many(vehicles)
        mongo_vehicles = [result for result in self.mongo_db.vehicles.find()]
        print('vehicles from Mongo DB:', mongo_vehicles)
        # return mongo_vehicles
        return

    def migrate_user_data(self):
        users = self.get_user_data()
        users = json.dumps(users)  # convert to str
        users = json.loads(users)  # convert to json
        for user in users:
            user_orders = self.get_user_orders(user['_id'])
            user['orders'] = user_orders

        self.mongo_db.users.insert_many(users)
        mongo_users = [result for result in self.mongo_db.users.find()]
        print('users from Mongo DB:', mongo_users)
        # return mongo_users
        return

    def get_user_orders(self, user_id):
        user_orders = '''
            SELECT order_id, vehicle_id, start_loc, destination, status, passengers
            FROM orders
            WHERE user_id = {}; 
        '''.format(user_id)
        orders = get_report(self.mysql, user_orders)

        orders_with_keys = []
        for result in orders:
            result = {
                'order_id': result[0],
                'vehicle_id': result[1],
                'start_loc': result[2],
                'destination': result[3],
                'status': result[4],
                'passengers': result[5]
            }
            orders_with_keys.append(result)

        hist_orders_with_keys = self.get_user_history_orders(user_id)
        all_orders_with_keys = orders_with_keys + hist_orders_with_keys
        return all_orders_with_keys

    def get_user_history_orders(self, user_id):
        user_history = '''
            SELECT order_id, vehicle_id, start_loc, destination, passengers, end_time, distance, trip_time, price
            FROM history_orders
            WHERE user_id = {}; 
        '''.format(user_id)
        hist_orders = get_report(self.mysql, user_history)

        hist_orders_with_keys = []
        for result in hist_orders:
            result = {
                'order_id': result[0],
                'vehicle_id': result[1],
                'start_loc': result[2],
                'destination': result[3],
                'status': 'completed',
                'passengers': result[4],
                'end_time': result[5],
                'distance': result[6],
                'trip_time': result[7],
                'price': result[8]
            }
            hist_orders_with_keys.append(result)

        return hist_orders_with_keys

    def get_user_data(self):
        user_data = '''
            SELECT user_id, name, email, password, balance
            FROM users; '''
        users = get_report(self.mysql, user_data)

        users_with_keys = []
        for result in users:
            result = {
                '_id': result[0],
                'name': result[1],
                'email': result[2],
                'password': result[3],
                'balance': result[4]
            }
            users_with_keys.append(result)
        return users_with_keys

    def get_vehicle_data(self):
        vehicle_data = '''
            SELECT vehicle_id, manufacturer, model, capacity, status, number_plate
            FROM vehicles
            JOIN models ON vehicles.model_id = models.model_id;'''
        vehicles = get_report(self.mysql, vehicle_data)

        vehicles_with_keys = []
        for result in vehicles:
            result = {
                '_id': result[0],
                'manufacturer': result[1],
                'model': result[2],
                'capacity': result[3],
                'status': result[4],
                'number_plate': result[5]
            }
            vehicles_with_keys.append(result)
        return vehicles_with_keys
