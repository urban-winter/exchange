'''
Stock exchange simulation

Submit orders
Cancel orders
View the order book
Match orders to create trades

'''
import unittest
from collections import namedtuple

Order = namedtuple('Order', 'buy_sell, quantity')
Trade = namedtuple('Trade', 'buy,sell')

class Exchange(object):
    
    def __init__(self):
        self._buy_order_book = []
        self._sell_order_book = []

    def submit_order(self,order):
        if order.buy_sell == 'buy':
            self._buy_order_book.append(order)
        else:
            self._sell_order_book.append(order)
    
    def order_book(self):
        return self._buy_order_book+self._sell_order_book
    
    def match_orders(self):
        trades = []
        for buy_order in self._buy_order_book:
            for sell_order in self._sell_order_book:
                if buy_order.quantity == sell_order.quantity:
                    trades.append(Trade(buy=buy_order, sell=sell_order))
        return trades

class TestExchange(unittest.TestCase):

    def test_can_retrieve_order(self):
        exchange = Exchange()
        order = Order('buy',1000)
        exchange.submit_order(order)
        orders = exchange.order_book()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0], order)
        
    def test_no_orders_no_matches(self):
        exchange = Exchange()
        matches = exchange.match_orders()
        self.assertEqual(matches, [])
        
# orders will match if there is a buy and sell order with same amount
# multiple sells, single buy
# multiple buys, single sell
# volumes don't match
        
    def test_match_orders(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].buy, buy_order)
        self.assertEqual(trades[0].sell, sell_order)

# check that orders are removed
# check that match price is reported

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()