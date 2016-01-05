'''
market_maker

always offer a buy and sell price
offered prices should be last traded price +- spread%/2
'''
import unittest
from exchange import Exchange, Order

#         buy_orders, sell_orders = exchange.find_orders('my counterparty id')


class MarketMaker(object):
    MARGIN = 0.02
    def __init__(self, exchange):
        self.exchange = exchange

    def trade(self):
        offer_price = self.exchange.last_trade()[0] * (1 - self.MARGIN/2)
        bid_price = self.exchange.last_trade()[0] * (1 + self.MARGIN/2)
        self.exchange.submit_order(Order('buy',123,offer_price))
        self.exchange.submit_order(Order('sell',456,bid_price))

class TestMarketMaker(unittest.TestCase):

    def test_no_current_orders(self):
        exchange = Exchange()
        mm = MarketMaker(exchange)
        mm.trade()
        self.assertEqual(len(exchange.order_book()), 2)
        # check order prices
        expected_offer = exchange.OPEN_DEFAULT_PRICE * (1 + mm.MARGIN/2)
        expected_bid = exchange.OPEN_DEFAULT_PRICE * (1 - mm.MARGIN/2)
        self.assertEqual(exchange.buy_order_book()[0].price, expected_bid)
        self.assertEqual(exchange.sell_order_book()[0].price, expected_offer)
        # check volumes
        
        
    # check that when a trade is completed the market maker trades are replaced
    # check that marker maker prices are based on order book prices


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()