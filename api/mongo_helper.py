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
        email = data['email']
        password = data['password']
        start = data['start']
        dest = data['dest']
        passengers = data['passengers']
        print('you are here in mongo create_order')
        user_id = self.get_user_id(email, password)
        print('user_id in mongo create_order:', user_id)
        return {'ride booking is not yet implemented'}

    def get_user_id(self, email, password):
        user_id = self.mongo_db.findOne({'email': email, 'password': password}, {'_id': 1})
        return user_id
