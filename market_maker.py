'''
market_maker

always offer a buy and sell price
offered prices should be last traded price +- spread%/2
'''
import unittest
from exchange import Exchange, Order

#         buy_orders, sell_orders = exchange.find_orders('my counterparty id')


class MarketMaker(object):
    
    def __init__(self, exchange):
        self.exchange = exchange

    def trade(self):
        self.exchange.submit_order(Order('buy',99))
        self.exchange.submit_order(Order('sell',101))

class TestMarketMaker(unittest.TestCase):

    def test_no_current_orders(self):
        exchange = Exchange()
        mm = MarketMaker(exchange)
        mm.trade()
        orders = exchange.order_book()
        self.assertEqual(len(orders), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()