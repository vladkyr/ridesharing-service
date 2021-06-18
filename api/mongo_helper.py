from time import time
from flask_pymongo import DESCENDING


class MongoHelper:
    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    def create_order(self, data):
        new_order = {
            '_id': int(time()),
            'start_loc': data['start'],
            'destination': data['dest'],
            'status': 'new',
            'passengers': data['passengers']
        }
        email = data['email']
        password = data['password']
        passengers = data['passengers']

        user_id = self.get_user_id(email, password)

        if user_id is None:  # no user in DB with such email and password
            return 'No user found in DB. Please check your email and password'
        else:
            try:
                passengers = int(passengers)
            except ValueError:
                return 'Incorrect number of passengers. Please type integer in field "passengers"'

            user_id = user_id['_id']
            vehicle_id = self.get_vehicle(passengers)

            mongo_user = self.mongo_db.users.find_one({'_id': user_id})
            print('user from Mongo DB:', mongo_user)

            if vehicle_id is None:  # no vehicle in DB available with enough capacity
                new_order['status'] = 'new, no vehicle'
                self.mongo_db.users.update_one({'_id': user_id}, {'$push': {'orders': new_order}})
            else:
                new_order['vehicle_id'] = vehicle_id
                print('new_order', new_order)
                self.mongo_db.users.update_one({'_id': user_id}, {'$push': {'orders': new_order}})

            mongo_user = self.mongo_db.users.find_one({'_id': user_id})
            print('user from Mongo DB after new order creation:', mongo_user)

        return 'Created new order in Mongo DB for user' + str(user_id) + ', orders of that user: ' + str(mongo_user)

    def get_user_id(self, email, password):
        user_id = self.mongo_db.users.find_one({'email': email, 'password': password}, {'_id': 1})
        return user_id

    def get_vehicle(self, passengers):
        vehicle_id = self.mongo_db.vehicles.find_one(
            {
                'capacity': {'$gte': passengers},
                'status': 'available'
            },
            {
                '_id': 1
            })

        return vehicle_id['_id']

    def get_most_popular_models(self):
        results = self.mongo_db.users.aggregate([
            # get list of all orders
            {
                '$unwind': '$orders'
            },
            # get respective model data for each vehicle in order
            {
                '$lookup': {
                    'from': 'vehicles',
                    'localField': 'orders.vehicle_id',
                    'foreignField': '_id',
                    'as': 'model'
                }
            },
            # select necessary data from each order
            {
                '$project': {
                    'manufacturer': {'$first': '$model.manufacturer'},
                    'model': {'$first': '$model.model'},
                    'capacity': {'$first': '$model.capacity'},
                    'vehicle_id': '$orders.vehicle_id',
                    'trip_time': '$orders.trip_time',
                    'status': '$orders.status',
                    'passengers': '$orders.passengers',
                    'end_time': {'$toDate': '$orders.end_time'},
                    'now_minus_order_end_time_lte_one_year': {
                        '$lte': [{'$subtract': ['$$NOW', {'$toDate': '$orders.end_time'}]}, (365 * 24 * 60 * 60 * 1000)]
                    }
                }
            },
            # select only completed orders and those which are within last year
            {
                '$match': {
                    'status': 'completed',
                    'now_minus_order_end_time_lte_one_year': True
                }
            },
            # group orders by vehicle model and compute several values
            {
                '$group': {
                    '_id': {'$concat': ['$manufacturer', '-', '$model', '-', {'$toString': '$capacity'}]},
                    'manufacturer': {'$first': '$manufacturer'},
                    'model': {'$first': '$model'},
                    'capacity': {'$first': '$capacity'},
                    'trips_number': {'$sum': 1},
                    'avg_trip_time': {'$avg': '$trip_time'},
                    'avg_passengers': {'$avg': '$passengers'}
                }
            },
            # sort results by number od trips (decreasing)
            {
                '$sort': {
                    'trips_number': DESCENDING
                }
            }
        ])

        results_list = []
        for result in results:
            result = {
                'manufacturer': result['manufacturer'],
                'model': result['model'],
                'capacity': result['capacity'],
                'trips': result['trips_number'],
                'avg_trip_time': int(result['avg_trip_time']),
                'avg_passengers': round(float(result['avg_passengers']), 1)
            }
            results_list.append(result)

        return results_list
