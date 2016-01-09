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
exchange.delete_my_orders
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
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
    def __str__(self):
        return 'Order( buy_sell=%s, quantity=%s, price=%s)' % (self.buy_sell, self.quantity, self.price)

class OrderBook(object):
    def __init__(self):
        self._orders = []
    def add(self, order, client_id):
        """Add an order to the book
        """
        self._orders.append(order)
    def delete(self, order):
        """Delete an order from the book
        """
        self._orders.remove(order)
    def orders(self):
        """Return a list of all orders in the book
        """
        return self._orders
    def highest_buy_order(self):
        """Return the buy order with the highest price or None if there are no buy orders
        """
#         buy_prices = [order.price for order in self._buy_order_book if order.price is not None]
#         sell_prices = [order.price for order in self._sell_order_book if order.price is not None]        pass
    def lowest_sell_order(self):
        """Return the sell order with the lowest price or None if there are no sell orders
        """
        pass
    def delete_orders_for_client(self, client_id):
        """Delete all orders associated with a specified client
        """
        pass

class TestOrderBook(unittest.TestCase):
    def test_add_order(self):
        order_book = OrderBook()
        test_order = Order('buy',1000,10.0)
        order_book.add(test_order, 1)
        self.assertEqual(order_book.orders(), [test_order])
    def test_delete_order(self):
        # add an order and confirm that it's there
        order_book = OrderBook()
        test_order = Order('buy',1000,10.0)
        order_book.add(test_order, 1)
        self.assertEqual(order_book.orders(), [test_order])
        # delete it and confirm that it's gone
        order_book.delete(test_order)
        self.assertEqual(order_book.orders(), [])
    def test_remove_all_orders_for_client(self):
        pass

# class Exchange(object):
#     # TODO: market orders
#     # TODO: partial fills, volumes not matching generally
#     OPEN_DEFAULT_PRICE = 100.0
#     
#     def __init__(self):
#         self._buy_order_book = OrderBook()
#         self._sell_order_book = OrderBook()
#         self._latest_price = self.OPEN_DEFAULT_PRICE
#         self._latest_volume = None
#         self._clients = []
#         self.current_client = None
# 
#     def submit_order(self,order):
#         if order.buy_sell == 'buy':
#             self._buy_order_book.add(order, self.current_client)
#         else:
#             self._sell_order_book.add(order, self.current_client)
#             
#     def submit_orders(self, orders):
#         map(self.submit_order, orders)
#     
#     def buy_order_book(self):
#         return self._buy_order_book.orders()
#     
#     def sell_order_book(self):
#         return self._sell_order_book.orders()        
# 
#     def order_book(self):
#         return self.buy_order_book()+self.sell_order_book()
#     
#     def match_orders(self):
#         trades = []
#         for buy_order in self._buy_order_book.orders():
#             for sell_order in self._sell_order_book.orders():
#                 if buy_order.quantity == sell_order.quantity:
#                     trades.append(Trade(buy=buy_order, sell=sell_order))
#                     self._sell_order_book.delete(sell_order)
#                     break
#         for trade in trades:
#             self._buy_order_book.delete(trade.buy)
#         if trades:
#             self._latest_price = trades[0].sell.price
#             self._latest_volume = trades[0].buy.quantity
#         return trades
#      
#     def bid_offer(self):
#         """Return bid, offer price
#         """
#         return self._buy_order_book.highest_buy_order(), self._sell_order_book.lowest_sell_order()
#     
#     def last_trade(self):
#         return self._latest_price, self._latest_volume
#     
#     def do_trading(self):
#         for client_id, client in enumerate(self._clients):
#             self.current_client = client_id
#             client(self)
#         self.current_client = None
#     
#     def add_client(self,client_callable):
#         self._clients.append(client_callable)
#         
# #     def _delete_order(self, order, order_book):
# #         """Delete an order from an order_book
# #         
# #         Orders cannot be removed directly because reference also
# #         needs to be removed from client_id_by_order.
# #         Order book really needs to be factored out as its own class
# #         """
# #         order_book.remove(order)
# #         del(self.client_id_by_order[order])
# #     
# #     def _delete_orders(self, order_book):
# #         for order in order_book:
# #             if self.client_id_by_order[order] == self.current_client:
# #                 self._delete_order(order, order_book)
#             
#     def delete_my_orders(self):
#         self._buy_order_book.delete_orders_for_client(self.current_client)
#         self._sell_order_book.delete_orders_for_client(self.current_client)
# 
# class TestClientFunctions(unittest.TestCase):
#     class DummyClient(object):
#         def __init__(self):
#             self.call_count = 0
#         def __call__(self,_):
#             self.call_count += 1
#     def order_submitting_client(self,exchange):
#         exchange.submit_order(Order('buy',1000,10.0))
#     def test_do_trading_with_no_clients(self):
#         exchange = Exchange()
#         exchange.do_trading()
#     def test_registered_client_is_called(self):
#         exchange = Exchange()
#         client = self.DummyClient()
#         exchange.add_client(client)
#         exchange.do_trading()
#         self.assertEqual(client.call_count,1)
#     def test_two_clients(self):
#         exchange = Exchange()
#         client1 = self.DummyClient()
#         exchange.add_client(client1)
#         client2 = self.DummyClient()
#         exchange.add_client(client2)
#         exchange.do_trading()
#         self.assertEqual(client1.call_count,1)
#         self.assertEqual(client2.call_count,1)
#     def test_client_can_submit_orders(self):
#         exchange = Exchange()
#         exchange.add_client(self.order_submitting_client)
#         exchange.do_trading()
#         self.assertEqual(exchange.order_book(), [Order('buy',1000,10.0)])
#     def test_client_trades_have_client_id(self):
#         exchange = Exchange()
#         exchange.add_client(self.order_submitting_client)
#         exchange.do_trading()
#         self.assertEqual(exchange.client_id_by_order.values(), [0])
#     def test_client_can_delete_own_orders(self):
#         exchange = Exchange()
#         exchange.current_client = 1
#         exchange.submit_order(Order('buy',10,1.0))
#         exchange.current_client = 2
#         exchange.submit_order(Order('sell',10,1.0))
#         self.assertEqual(len(exchange.order_book()), 2)
#         exchange.delete_my_orders()
#         self.assertEqual(exchange.order_book(), [Order('buy',10,1.0)])
#         self.assertEqual(exchange.client_id_by_order.values(), [1])
#     
# class TestPriceDerivation(unittest.TestCase):
#     def test_no_price(self):
#         exchange = Exchange()
#         buy_order = Order('buy',1000)
#         sell_order = Order('sell',1000)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order)
#         bid, offer = exchange.bid_offer()
#         self.assertEqual(bid, None)
#         self.assertEqual(offer, None)
#     def test_offer_price_only(self):
#         exchange = Exchange()
#         buy_order = Order('buy',1000)
#         sell_order = Order('sell',1000,10.0)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order)
#         bid, offer = exchange.bid_offer()
#         self.assertEqual(bid, None)
#         self.assertEqual(offer, 10.0)
#     def test_bid_price_only(self):
#         exchange = Exchange()
#         buy_order = Order('buy',1000,10.0)
#         sell_order = Order('sell',1000)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order)
#         bid, offer = exchange.bid_offer()
#         self.assertEqual(bid, 10.0)
#         self.assertEqual(offer, None)
#     def test_multiple_priced_and_unpriced_buys_and_sells(self):
#         orders = (Order('buy',1000,10.0),Order('buy',1000,10.1),Order('buy',1000),
#                   Order('sell',1000,11.0),Order('sell',1000,11.1),Order('sell',1000))
#         exchange = Exchange()
#         exchange.submit_orders(orders)
#         bid, offer = exchange.bid_offer()
#         self.assertEqual(bid, 10.1)
#         self.assertEqual(offer, 11.0)
#     def test_last_traded_when_no_trades(self):
#         exchange = Exchange()
#         last_traded_price, last_traded_volume = exchange.last_trade()
#         self.assertEqual(last_traded_price, exchange.OPEN_DEFAULT_PRICE)
#         self.assertEqual(last_traded_volume, None)
#     def test_last_traded_when_a_completed_trade(self):
#         exchange = Exchange()
#         buy_order = Order('buy',1000,10.0)
#         sell_order = Order('sell',1000,9.9)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order)
#         trades = exchange.match_orders()
#         last_traded_price, last_traded_volume = exchange.last_trade()
#         self.assertEqual(last_traded_price, 9.9)
#         self.assertEqual(last_traded_volume, 1000)
#         
# class TestExchange(unittest.TestCase):
# 
#     def test_can_retrieve_order(self):
#         exchange = Exchange()
#         order = Order('buy',1000)
#         exchange.submit_order(order)
#         orders = exchange.order_book()
#         self.assertEqual(len(orders), 1)
#         self.assertEqual(orders[0], order)
#         
#     def test_no_orders_no_matches(self):
#         exchange = Exchange()
#         matches = exchange.match_orders()
#         self.assertEqual(matches, [])
# 
# # TODO: buy higher than sell matches
# # TODO: buy lower than sell doesn't match
# 
#     def test_match_orders(self):
#         exchange = Exchange()
#         buy_order = Order('buy',1000)
#         sell_order = Order('sell',1000)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order)
#         trades = exchange.match_orders()
#         self.assertEqual(len(trades), 1)
#         self.assertEqual(trades[0].buy, buy_order)
#         self.assertEqual(trades[0].sell, sell_order)
#         
#     def test_matched_orders_removed_from_order_book(self):
#         exchange = Exchange()
#         exchange.current_client = 1
#         buy_order = Order('buy',1000)
#         sell_order = Order('sell',1000)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order)
#         exchange.match_orders()
#         orders = exchange.order_book()
#         self.assertEqual(orders, [])
#         self.assertEqual(exchange.client_id_by_order.values(), [])
# 
#     def test_not_matching_orders_dont_match(self):
#         exchange = Exchange()
#         buy_order = Order('buy',1000)
#         sell_order = Order('sell',999)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order)
#         trades = exchange.match_orders()
#         self.assertEqual(trades, [])
#         self.assertEqual(len(exchange.order_book()), 2)
#         
#     def test_multiple_sells_single_buy(self):
#         exchange = Exchange()
#         buy_order = Order('buy',1000)
#         sell_order_1 = Order('sell',1000)
#         sell_order_2 = Order('sell',1000)
#         exchange.submit_order(buy_order)
#         exchange.submit_order(sell_order_1)
#         exchange.submit_order(sell_order_2)
#         trades = exchange.match_orders()
#         self.assertEqual(len(trades), 1)
#         self.assertEqual(trades[0].buy, buy_order)
#         self.assertEqual(trades[0].sell, sell_order_1)
#         self.assertEqual(len(exchange.order_book()), 1)
#         self.assertEqual(exchange.order_book()[0], sell_order_2)
#         
#     def test_multiple_buys_single_sell(self):
#         exchange = Exchange()
#         buy_order_1 = Order('buy',1000)
#         buy_order_2 = Order('buy',1000)
#         sell_order = Order('sell',1000)
#         exchange.submit_order(buy_order_1)
#         exchange.submit_order(buy_order_2)
#         exchange.submit_order(sell_order)
#         trades = exchange.match_orders()
#         self.assertEqual(len(trades), 1)
#         self.assertEqual(trades[0].buy, buy_order_1)
#         self.assertEqual(trades[0].sell, sell_order)
#         self.assertEqual(len(exchange.order_book()), 1)
#         self.assertEqual(exchange.order_book()[0], buy_order_2)
# 
# if __name__ == "__main__":
#     #import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()