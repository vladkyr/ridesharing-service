from time import time

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
                self.mongo_db.users.update_one({'_id': user_id}, {'$addToSet': {'orders': new_order}})
            else:
                new_order['vehicle_id'] = vehicle_id
                print('new_order', new_order)
                self.mongo_db.users.update_one({'_id': user_id}, {'$addToSet': {'orders': new_order}})

            mongo_user = self.mongo_db.users.find_one({'_id': user_id})
            print('user from Mongo DB after update:', mongo_user)

        return 'Created new order in Mongo DB for user' + str(user_id) + ': ' + str(mongo_user)

    def get_user_id(self, email, password):
        # mongo_users = [result for result in self.mongo_db.users.find()]
        # print('users from Mongo DB:', mongo_users)
        user_id = self.mongo_db.users.find_one({'email': email, 'password': password}, {'_id': 1})
        return user_id

    def get_vehicle(self, passengers):
        vehicle_id = self.mongo_db.vehicles.find_one({'capacity': {'$gte': passengers}, 'status': 'available'}, {'_id': 1})
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
