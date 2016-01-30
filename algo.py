'''
Create a stream of buy and sell orders
Execute them on the exchange
'''
import unittest
from exchange import Order

def order_gen():
    while True:
        yield Order(buy_sell='buy',quantity=1000)

class TestOrderGenerator(unittest.TestCase):


    def testOneOrder(self):
        orders = order_gen()
        order = next(orders)
        self.assertTrue(hasattr(order,'buy_sell'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()