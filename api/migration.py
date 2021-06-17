import json
from func import get_report


class MigrationHelper:
    def __init__(self, mysql):
        self.mysql = mysql

    def migrate_data(self):
        vehicles = self.get_vehicle_data()
        users = self.get_user_data()
        users = json.dumps(users)  # convert to str
        users = json.loads(users)  # convert to json
        for user in users:
            user_orders = self.get_user_orders(user['user_id'])
            print('user_id', user['user_id'])
            print('\n(all_orders_with_keys) user_orders:', user_orders)
            user['orders'] = user_orders
            print('\nuser', user)

        return {'vehicle_data': vehicles, 'user_data': users}
        # return {'message': "Data successfully migrated from Mysql to Mongo"}

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

        all_orders_with_keys = orders_with_keys + hist_orders_with_keys
        return all_orders_with_keys

    def get_user_data(self):
        user_data = '''
            SELECT user_id, name, email, password, balance
            FROM users; 
        '''
        users = get_report(self.mysql, user_data)

        users_with_keys = []
        for result in users:
            result = {
                'user_id': result[0],
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
            JOIN models ON vehicles.model_id = models.model_id; 
        '''
        vehicles = get_report(self.mysql, vehicle_data)

        vehicles_with_keys = []
        for result in vehicles:
            result = {
                'vehicle_id': result[0],
                'manufacturer': result[1],
                'model': result[2],
                'capacity': result[3],
                'status': result[4],
                'number_plate': result[5]
            }
            vehicles_with_keys.append(result)
        return vehicles_with_keys
