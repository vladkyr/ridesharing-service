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
