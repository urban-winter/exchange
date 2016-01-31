'''
Create a stream of buy and sell orders
Execute them on the exchange

eventually the order generation will be a separate component from the algo
'''
import unittest
from exchange import Order
from mock import Mock
from itertools import islice, ifilter
import random

def buy_sell_function():    
    return random.choice(['buy','sell'])

def order_gen(buy_sell_function=buy_sell_function):
    while True:
        yield Order(buy_sell=buy_sell_function(),quantity=1000)

class TestOrderGenerator(unittest.TestCase):

    def test_one_order(self):
        orders = order_gen()
        order = next(orders)
        self.assertTrue(hasattr(order,'buy_sell'))
        self.assertTrue(hasattr(order,'quantity'))        
    def test_order_is_buy(self):
        # Given a buy_sell_function that returns 'buy'
        buy_sell_mock = Mock()
        buy_sell_mock.return_value = 'buy'
        orders = order_gen(buy_sell_function = buy_sell_mock)
        # when next(order_gen) is called
        order = next(orders)
        # then the returned order is a buy order
        self.assertEqual(order.buy_sell, 'buy')
    def test_order_is_sell(self):
        # Given a buy_sell_function that returns 'sell'
        buy_sell_mock = Mock()
        buy_sell_mock.return_value = 'sell'
        orders = order_gen(buy_sell_function = buy_sell_mock)
        # when next(order_gen) is called
        order = next(orders)
        # then the returned order is a sell order
        self.assertEqual(order.buy_sell, 'sell')
    def test_buy_sell_is_random(self):
        # When 100 orders are generated
        # Then some, but not not all of them are buy order
        buy_orders = list(ifilter( lambda x: x.buy_sell == 'buy', islice(order_gen(),100)))
        self.assertTrue(len(buy_orders) > 0)
        self.assertTrue(len(buy_orders) < 100)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()