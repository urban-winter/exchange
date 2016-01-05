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
    ORDER_QUANTITY = 100
    def __init__(self, exchange):
        self.exchange = exchange

    def trade(self):
        # TODO: remove any of my existing orders
        offer_price = self.exchange.last_trade()[0] * (1 - self.MARGIN/2)
        bid_price = self.exchange.last_trade()[0] * (1 + self.MARGIN/2)
        self.exchange.submit_order(Order('buy',self.ORDER_QUANTITY,offer_price))
        self.exchange.submit_order(Order('sell',self.ORDER_QUANTITY,bid_price))

class TestMarketMaker(unittest.TestCase):

    def test_no_current_orders(self):
        exchange = Exchange()
        mm = MarketMaker(exchange)
        mm.trade()
        # check order prices and volumes
        self.assertEqual(len(exchange.order_book()), 2)
        expected_offer = exchange.OPEN_DEFAULT_PRICE * (1 + mm.MARGIN/2)
        expected_bid = exchange.OPEN_DEFAULT_PRICE * (1 - mm.MARGIN/2)
        self.assertEqual(exchange.buy_order_book()[0].price, expected_bid)
        self.assertEqual(exchange.sell_order_book()[0].price, expected_offer)
        self.assertEqual(exchange.buy_order_book()[0].quantity, mm.ORDER_QUANTITY)
        self.assertEqual(exchange.sell_order_book()[0].quantity, mm.ORDER_QUANTITY)
        
    def test_market_maker_trade_completed(self):
        exchange = Exchange()
        mm = MarketMaker(exchange)
        mm.trade()
        exchange.submit_order(Order('buy',100,exchange.OPEN_DEFAULT_PRICE * (1 + mm.MARGIN/2)))
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 1)
        mm.trade()
        # price should have gone up
        price, volume = exchange.last_trade()
        self.assertEqual(price, exchange.OPEN_DEFAULT_PRICE * (1 + mm.MARGIN/2))
        # old mm orders should have been removed
        # new mm offers should be based on new price
        # check order prices and volumes
        self.assertEqual(len(exchange.order_book()), 2)
        expected_offer = price * (1 + mm.MARGIN/2)
        expected_bid = price * (1 - mm.MARGIN/2)
        self.assertEqual(exchange.buy_order_book()[0].price, expected_bid)
        self.assertEqual(exchange.sell_order_book()[0].price, expected_offer)
        self.assertEqual(exchange.buy_order_book()[0].quantity, mm.ORDER_QUANTITY)
        self.assertEqual(exchange.sell_order_book()[0].quantity, mm.ORDER_QUANTITY)
        
        
    # check that when a trade is completed the market maker trades are replaced
    # check that marker maker prices are based on order book prices


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()