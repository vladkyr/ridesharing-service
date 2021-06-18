from time import time
from flask_pymongo import DESCENDING


class MongoHelper:
    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    def mongo_test(self):
        print('mongo_db', self.mongo_db)
        print('mongo_db.orders.find()', [result for result in self.mongo_db.orders.find()])
        self.mongo_db.orders.insert_one({
            '_id': 12345,
            'user': 'userX',
            'start': 'start1',
            'dest': 'dest1'
        })
        orders = [result for result in self.mongo_db.orders.find()]
        print('orders', orders)
        return orders

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
        # print('user_id of user who wants to create order:', user_id)

        if user_id is None:  # no user in DB with such email and password
            return 'No user found in DB. Please check your email and password'
        else:
            user_id = user_id['_id']
            vehicle_id = self.get_vehicle(passengers)

            mongo_user = self.mongo_db.users.find_one({'_id': user_id})
            print('user from Mongo DB:', mongo_user)

            if vehicle_id is None:  # no vehicle in DB available with enough capacity
                new_order['status'] = 'new, no vehicle'
                # self.mongo_db.users.update_one({'_id': user_id}, {'$addToSet': {'orders': new_order}})
                self.mongo_db.users.update_one({'_id': user_id}, {'$push': {'orders': new_order}})
            else:
                new_order['vehicle_id'] = vehicle_id
                print('new_order', new_order)
                # self.mongo_db.users.update_one({'_id': user_id}, {'$addToSet': {'orders': new_order}})
                self.mongo_db.users.update_one({'_id': user_id}, {'$push': {'orders': new_order}})

            mongo_user = self.mongo_db.users.find_one({'_id': user_id})
            print('user from Mongo DB after update:', mongo_user)

        return 'Created new order in Mongo DB for user' + str(user_id) + ': ' + str(mongo_user)

    def get_user_id(self, email, password):
        # mongo_users = [result for result in self.mongo_db.users.find()]
        # print('users from Mongo DB:', mongo_users)
        user_id = self.mongo_db.users.find_one({'email': email, 'password': password}, {'_id': 1})
        return user_id

    def get_vehicle(self, passengers):
        vehicle_id = self.mongo_db.vehicles.find_one({'capacity': {'$gte': passengers}, 'status': 'available'},
                                                     {'_id': 1})
        print('found vehicle', vehicle_id)

        vehicles = self.mongo_db.vehicles.find()
        print('all vehicles', [vehicle for vehicle in vehicles])
        vehicles = self.mongo_db.vehicles.find({'capacity': {'$gte': passengers}})
        print('all vehicles with capacity > passengers', [vehicle for vehicle in vehicles])
        vehicles = self.mongo_db.vehicles.find({'status': 'available'})
        print('all vehicles status available', [vehicle for vehicle in vehicles])
        vehicles = self.mongo_db.vehicles.find({'capacity': {'$gte': passengers}, 'status': 'available'})
        print('all vehicles with capacity > passengers and status available', [vehicle for vehicle in vehicles])

        return vehicle_id

    def get_most_popular_models(self):
        results = self.mongo_db.vehicles.find()
        print('\n\nvehicles:')
        for result in results:
            print(result)
        print('\n\n')

        results = self.mongo_db.users.find()
        print('\n\nusers:')
        for result in results:
            print(result)
        print('\n\n')

        results = self.mongo_db.users.aggregate([
            {
                '$unwind': '$orders'
            }
        ])
        print('\n\nresults x:')
        for result in results:
            print(result)
        print('\n\n')

        results = self.mongo_db.users.aggregate([
            {
                '$unwind': '$orders'
            },
            {
                '$lookup': {
                    'from': 'vehicles',
                    'localField': 'orders.vehicle_id',
                    'foreignField': '_id',
                    'as': 'model'
                }
            }
        ])
        print('\n\nresults x2:')
        for result in results:
            print(result)
        print('\n\n')

        results = self.mongo_db.users.aggregate([
            {
                '$unwind': '$orders'
            },
            {
                '$lookup': {
                    'from': 'vehicles',
                    'localField': 'orders.vehicle_id',
                    'foreignField': '_id',
                    'as': 'model'
                }
            },
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
                    'curr_datetime': '$$NOW',
                    'curr_datetime_minus_year': {'$subtract': ['$$NOW', (365 * 24 * 60 * 60 * 1000)]}
                }
            }
        ])
        print('\n\nresults x3:')
        for result in results:
            print(result)
        print('\n\n')

        results = self.mongo_db.users.aggregate([
            {
                '$unwind': '$orders'
            },
            {
                '$lookup': {
                    'from': 'vehicles',
                    'localField': 'orders.vehicle_id',
                    'foreignField': '_id',
                    'as': 'model'
                }
            },
            {
                '$project': {
                    'manufacturer': {'$first': '$model.manufacturer'},
                    'model': {'$first': '$model.model'},
                    'capacity': {'$first': '$model.capacity'},
                    'vehicle_id': '$orders.vehicle_id',
                    'trip_time': '$orders.trip_time',
                    'status': '$orders.status',
                    'passengers': '$orders.passengers',
                    'end_time': {'$toDate': '$orders.end_time'}
                }
            },
            {
                '$match': {
                    'status': 'completed'
                }
            }
        ])
        print('\n\nresults x4:')
        for result in results:
            print(result)
        print('\n\n')

        results = self.mongo_db.users.aggregate([
            {
                '$unwind': '$orders'
            },
            {
                '$lookup': {
                    'from': 'vehicles',
                    'localField': 'orders.vehicle_id',
                    'foreignField': '_id',
                    'as': 'model'
                }
            },
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
                    'curr_datetime': '$$NOW',
                    'curr_datetime_minus_year': {'$toDate': {'$subtract': ['$$NOW', (365 * 24 * 60 * 60 * 1000)]}}
                }
            },
            {
                '$match': {
                    'status': 'completed',
                    'end_time': {'$gte': {'$toDate': {'$subtract': ['$$NOW', (365 * 24 * 60 * 60 * 1000)]}}}
                }
            }
        ])
        print('\n\nresults x4.2:')
        for result in results:
            print(result)
        print('\n\n')

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
                    'end_time': '$orders.end_time'
                }
            },
            # select only completed orders
            {
                '$match': {
                    'status': 'completed'
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
        print('\n\nresults x5:')
        for result in results:
            print(result)
        print('\n\n')

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
                    'curr_datetime': '$$NOW',
                    'curr_datetime_minus_year': {'$subtract': ['$$NOW', (365 * 24 * 60 * 60 * 1000)]}
                }
            },
            # select only completed orders and those which are within last year
            {
                '$match': {
                    'status': 'completed'
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
        '''print('\n\nresults x6:')
        for result in results:
            print(result)
        print('\n\n')'''

        print('results', results)

        results_list = []
        for result in results:
            print('result:', result)
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
