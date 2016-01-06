'''
Stock exchange simulation

Submit orders
Cancel orders
View the order book
Match orders to create trades

Useful link:
http://stackoverflow.com/questions/13112062/which-are-the-order-matching-algorithms-most-commonly-used-by-electronic-financi

market clients register with the exchange
exchange.do_trading calls all
exchange.delete_my_trades
'''
import unittest
from collections import namedtuple

Trade = namedtuple('Trade', 'buy,sell')

class Order(object):
    # TODO: consider subclasses for buy and sell
    def __init__(self,buy_sell,quantity,price=None):
        self.buy_sell = buy_sell
        self.quantity = quantity
        self.price = price

class Exchange(object):
    # TODO: market orders
    # TODO: partial fills, volumes not matching generally
    OPEN_DEFAULT_PRICE = 100.0
    
    def __init__(self):
        self._buy_order_book = []
        self._sell_order_book = []
        self._latest_price = self.OPEN_DEFAULT_PRICE
        self._latest_volume = None
        self._clients = []

    def submit_order(self,order):
        if order.buy_sell == 'buy':
            self._buy_order_book.append(order)
        else:
            self._sell_order_book.append(order)
            
    def submit_orders(self, orders):
        map(self.submit_order, orders)
    
    def buy_order_book(self):
        return self._buy_order_book
    
    def sell_order_book(self):
        return self._sell_order_book        

    def order_book(self):
        return self.buy_order_book()+self.sell_order_book()
    
    def match_orders(self):
        trades = []
        for buy_order in self._buy_order_book:
            for sell_order in self._sell_order_book:
                if buy_order.quantity == sell_order.quantity:
                    trades.append(Trade(buy=buy_order, sell=sell_order))
                    self._sell_order_book.remove(sell_order)
                    break
        for trade in trades:
            self._buy_order_book.remove(trade.buy)
        if trades:
            self._latest_price = trades[0].sell.price
            self._latest_volume = trades[0].buy.quantity
        return trades
     
    def bid_offer(self):
        """Return bid, offer prices
        """
        buy_prices = [order.price for order in self._buy_order_book if order.price is not None]
        sell_prices = [order.price for order in self._sell_order_book if order.price is not None]
        return max(buy_prices) if buy_prices else None, min(sell_prices) if sell_prices else None
    
    def last_trade(self):
        return self._latest_price, self._latest_volume
    
    def do_trading(self):
        for client in self._clients:
            client()
    
    def add_client(self,client_callable):
        self._clients.append(client_callable)

class TestClientRegistration(unittest.TestCase):
    client_call_count = 0
    def dummy_client(self):
        self.client_call_count += 1
    def test_do_trading_with_no_clients(self):
        exchange = Exchange()
        exchange.do_trading()
    def test_registered_client_is_called(self):
        exchange = Exchange()
        exchange.add_client(self.dummy_client)
        exchange.do_trading()
        self.assertEqual(self.client_call_count, 1)
        
    
class TestPriceDerivation(unittest.TestCase):
    def test_no_price(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        bid, offer = exchange.bid_offer()
        self.assertEqual(bid, None)
        self.assertEqual(offer, None)
    def test_offer_price_only(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000,10.0)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        bid, offer = exchange.bid_offer()
        self.assertEqual(bid, None)
        self.assertEqual(offer, 10.0)
    def test_bid_price_only(self):
        exchange = Exchange()
        buy_order = Order('buy',1000,10.0)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        bid, offer = exchange.bid_offer()
        self.assertEqual(bid, 10.0)
        self.assertEqual(offer, None)
    def test_multiple_priced_and_unpriced_buys_and_sells(self):
        orders = (Order('buy',1000,10.0),Order('buy',1000,10.1),Order('buy',1000),
                  Order('sell',1000,11.0),Order('sell',1000,11.1),Order('sell',1000))
        exchange = Exchange()
        exchange.submit_orders(orders)
        bid, offer = exchange.bid_offer()
        self.assertEqual(bid, 10.1)
        self.assertEqual(offer, 11.0)
    def test_last_traded_when_no_trades(self):
        exchange = Exchange()
        last_traded_price, last_traded_volume = exchange.last_trade()
        self.assertEqual(last_traded_price, exchange.OPEN_DEFAULT_PRICE)
        self.assertEqual(last_traded_volume, None)
    def test_last_traded_when_a_completed_trade(self):
        exchange = Exchange()
        buy_order = Order('buy',1000,10.0)
        sell_order = Order('sell',1000,9.9)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        trades = exchange.match_orders()
        last_traded_price, last_traded_volume = exchange.last_trade()
        self.assertEqual(last_traded_price, 9.9)
        self.assertEqual(last_traded_volume, 1000)
        
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
        
    def test_matched_orders_removed_from_order_book(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        exchange.match_orders()
        orders = exchange.order_book()
        self.assertEqual(orders, [])

    def test_not_matching_orders_dont_match(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',999)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        trades = exchange.match_orders()
        self.assertEqual(trades, [])
        self.assertEqual(len(exchange.order_book()), 2)
        
    def test_multiple_sells_single_buy(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order_1 = Order('sell',1000)
        sell_order_2 = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order_1)
        exchange.submit_order(sell_order_2)
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].buy, buy_order)
        self.assertEqual(trades[0].sell, sell_order_1)
        self.assertEqual(len(exchange.order_book()), 1)
        self.assertEqual(exchange.order_book()[0], sell_order_2)
        
    def test_multiple_buys_single_sell(self):
        exchange = Exchange()
        buy_order_1 = Order('buy',1000)
        buy_order_2 = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order_1)
        exchange.submit_order(buy_order_2)
        exchange.submit_order(sell_order)
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].buy, buy_order_1)
        self.assertEqual(trades[0].sell, sell_order)
        self.assertEqual(len(exchange.order_book()), 1)
        self.assertEqual(exchange.order_book()[0], buy_order_2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()