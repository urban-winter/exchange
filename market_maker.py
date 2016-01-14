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

    def __call__(self, exchange):
        exchange.delete_my_orders()
        current_bid, current_offer = exchange.bid_offer()
        bid_price = current_bid * (1 - self.MARGIN/2)
        offer_price = current_offer * (1 + self.MARGIN/2)
        exchange.submit_order(Order('buy',self.ORDER_QUANTITY,bid_price))
        exchange.submit_order(Order('sell',self.ORDER_QUANTITY,offer_price))

class TestMarketMaker(unittest.TestCase):

    def test_no_current_orders(self):
        exchange = Exchange()
        exchange.add_client(MarketMaker())
        exchange.do_trading()
        # check order prices and volumes
        self.assertEqual(len(exchange.order_book()), 2)
        expected_offer = exchange.OPEN_DEFAULT_PRICE * (1 + MarketMaker.MARGIN/2)
        expected_bid = exchange.OPEN_DEFAULT_PRICE * (1 - MarketMaker.MARGIN/2)
        self.assertEqual(exchange.buy_order_book()[0].price, expected_bid)
        self.assertEqual(exchange.sell_order_book()[0].price, expected_offer)
        self.assertEqual(exchange.buy_order_book()[0].quantity, MarketMaker.ORDER_QUANTITY)
        self.assertEqual(exchange.sell_order_book()[0].quantity, MarketMaker.ORDER_QUANTITY)
        
    def test_market_maker_trade_completed(self):
        # This test is too complicated!
        exchange = Exchange()
        exchange.add_client(MarketMaker())
        exchange.do_trading()
        # Should be two orders at this point
        self.assertEqual(len(exchange.order_book()), 2)
        exchange.submit_order(Order('buy',100,exchange.OPEN_DEFAULT_PRICE * (1 + MarketMaker.MARGIN)))
        self.assertEqual(len(exchange.order_book()), 3)
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 1)
        exchange.do_trading()
        # price should have gone up
        price, volume = exchange.last_trade()
        self.assertEqual(price, exchange.OPEN_DEFAULT_PRICE * (1 + MarketMaker.MARGIN/2))
        # old mm orders should have been removed
        # new mm offers should be based on new price
        # check order prices and volumes
        self.assertEqual(len(exchange.order_book()), 2)
        expected_offer = price * (1 + MarketMaker.MARGIN/2)
        expected_bid = price * (1 - MarketMaker.MARGIN/2)
        self.assertEqual(exchange.buy_order_book()[0].price, expected_bid)
        self.assertEqual(exchange.sell_order_book()[0].price, expected_offer)
        self.assertEqual(exchange.buy_order_book()[0].quantity, MarketMaker.ORDER_QUANTITY)
        self.assertEqual(exchange.sell_order_book()[0].quantity, MarketMaker.ORDER_QUANTITY)
        
    # check that marker maker prices are based on order book prices
    def test_market_maker_price(self):
        # scenario: check that marker maker prices are based on order book prices
        exchange = Exchange()
        # given an order book with a buy order with price 10.0
        exchange.current_client = 99
        exchange.submit_order(Order('buy',100,10.0))        
        # and the market maker is a client of the exchange
        exchange.add_client(MarketMaker())
        # when do_trading is called
        exchange.do_trading()
        # the order book contains a buy order with price 10.0 - MARGIN/2
        # and the original buy at 10.0
        self.assertEqual(exchange.buy_order_book(), 
                         [Order('buy',100,10.0),
                          Order('buy',100,10.0 * (1 - MarketMaker.MARGIN/2))])
        # and a sell order with price 10 + MARGIN/2
        self.assertEqual(exchange.sell_order_book(),
                         [Order('sell',100,10.0 * (1 + MarketMaker.MARGIN/2))])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()