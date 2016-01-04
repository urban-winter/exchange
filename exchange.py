'''
Stock exchange simulation

Submit orders
Cancel orders
View the order book
Match orders to create trades

'''
import unittest
from collections import namedtuple

Order = namedtuple('Order', 'buy_sell, amount')

class Exchange(object):
    
    def __init__(self):
        self._order_book = []

    def submit_order(self,order):
        self._order_book.append(order)
    
    def order_book(self):
        return self._order_book

class TestExchange(unittest.TestCase):


    def test_can_retrieve_order(self):
        exchange = Exchange()
        order = Order('buy',1000)
        exchange.submit_order(order)
        orders = exchange.order_book()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0], order)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()