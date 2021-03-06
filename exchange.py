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
from locale import currency
import logging

Trade = namedtuple('Trade', 'buy,sell,price')

logger = logging.getLogger(__name__)

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
    def __str__(self):
        elems = []
        elems.append('OrderBook')
        elems.append('Buys')
        # TODO: helper function for formatting
        elems.extend([str(order) for order in self.buy_orders()] if len(self.buy_orders()) else ['Empty'])
        elems.append('Sells')
        elems.extend([str(order) for order in self.sell_orders()] if len(self.sell_orders()) else ['Empty'])
        return '\n'.join(elems)
        
    def add(self, order, client_id):
        """Add an order to the book
        """
        self._orders.append((client_id,order))
    def delete(self, order_to_delete):
        """Delete an order from the book
        """
        for (client_id,order) in self._orders:
            if order == order_to_delete:
                self._orders.remove((client_id,order))
    def orders(self):
        """Return a list of all orders in the book
        """
        return [order for (_,order) in self._orders]
    def highest_buy_order(self):
        """Return the buy order with the highest price or None if there are no buy orders
        """
        buy_prices = [order.price for (_,order) in self._orders 
                        if order.price is not None 
                        and order.buy_sell == 'buy']
        return max(buy_prices) if buy_prices else None
#         sell_prices = [order.price for order in self._sell_order_book if order.price is not None]        pass
    def lowest_sell_order(self):
        """Return the sell order with the lowest price or None if there are no sell orders
        """
        sell_prices = [order.price for (_,order) in self._orders 
                        if order.price is not None 
                        and order.buy_sell == 'sell']
        return min(sell_prices) if sell_prices else None
    def delete_orders_for_client(self, client_id_to_delete):
        """Delete all orders associated with a specified client
        """
        for (client_id,order) in self._orders:
            if client_id == client_id_to_delete:
                self._orders.remove((client_id,order))
    def buy_orders(self):
        """Return all buy orders in the book"""
        return [order for (_,order) in self._orders if order.buy_sell == 'buy']
    def sell_orders(self):
        """Return all sell orders in the book"""
        return [order for (_,order) in self._orders if order.buy_sell == 'sell']
    def client_id_for(self, order):
        """Return the client ID associated with the specified trade"""
        for (client_id,order_in_book) in self._orders:
            if order_in_book == order:
                return client_id

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
    def test_highest_buy_order_1(self):
        # given an empty order book
        order_book = OrderBook()
        # then the highest buy order should be none
        self.assertEqual(order_book.highest_buy_order(), None)
    def test_highest_buy_order_2(self):
        # given a book with only sell orders
        order_book = OrderBook()
        order_book.add(Order('sell', 1000, 10.0), 0)
        # then the highest buy order should be none
        self.assertEqual(order_book.highest_buy_order(), None)        
    def test_highest_buy_order_3(self):
        # given a book with 2 buy orders
        order_book = OrderBook()
        order_book.add(Order('buy', 1000, 10.0), 0)
        order_book.add(Order('buy', 1000, 10.1), 0)
        # then the highest buy order should be the higher
        self.assertEqual(order_book.highest_buy_order(), 10.1)        
    def test_lowest_sell_order_1(self):
        # given an empty order book
        order_book = OrderBook()
        # then the lowest sell order should be none
        self.assertEqual(order_book.lowest_sell_order(), None)
    def test_lowest_sell_order_2(self):
        # given a book with only buy orders
        order_book = OrderBook()
        order_book.add(Order('buy', 1000, 10.0), 0)
        # then the lowest sell order should be none
        self.assertEqual(order_book.lowest_sell_order(), None)        
    def test_lowest_sell_order_3(self):
        # given a book with 2 sell orders
        order_book = OrderBook()
        order_book.add(Order('sell', 1000, 10.0), 0)
        order_book.add(Order('sell', 1000, 10.1), 0)
        # then the lowest sell order should be the lower
        self.assertEqual(order_book.lowest_sell_order(), 10.0)        
    def test_remove_all_orders_for_client_1(self):
        # given an order book with 1 order for each of 2 clients
        order_book = OrderBook()
        order_book.add(Order('buy',1000,10.0), 0)
        order_book.add(Order('buy',1001,10.1), 1)
        # when the order for one client is removed
        order_book.delete_orders_for_client(0)
        # then the order for that client is no longer present
        # and the order for the other client is still present
        self.assertEqual(order_book.orders(), [Order('buy',1001,10.1)])
    def test_buy_orders(self):
        # given an order book with a buy and a sell order
        order_book = OrderBook()
        order_book.add(Order('buy',1000,10.0), 0)
        order_book.add(Order('sell',1001,10.1), 1)        
        # when buy_orders is called
        # only the buy order is returned
        self.assertEqual(order_book.buy_orders(), [Order('buy',1000,10.0)])
    def test_sell_orders(self):
        # given an order book with a buy and a sell order
        order_book = OrderBook()
        order_book.add(Order('buy',1000,10.0), 0)
        order_book.add(Order('sell',1001,10.1), 1)        
        # when sell_orders is called
        # only the sell order is returned
        self.assertEqual(order_book.sell_orders(), [Order('sell',1001,10.1)])

class Exchange(object):
    # TODO: market orders
    # TODO: partial fills, volumes not matching generally
    OPEN_DEFAULT_PRICE = 100.0
     
    def __init__(self):
        self._order_book = OrderBook()
        self._latest_price = self.OPEN_DEFAULT_PRICE
        self._latest_volume = None
        self._clients = []
        self.current_client = None
 
    def submit_order(self,order):
        self._order_book.add(order, self.current_client)
             
    def submit_orders(self, orders):
        map(self.submit_order, orders)
     
    def buy_order_book(self):
        return self._order_book.buy_orders()
     
    def sell_order_book(self):
        return self._order_book.sell_orders()        
 
    def order_book(self):
        return self._order_book.orders()
    
    def order_matches(self, buy_order, sell_order):
        if (buy_order.quantity == sell_order.quantity and 
            self._order_book.client_id_for(buy_order) != self._order_book.client_id_for(sell_order)):
            return match_order(self._latest_price, buy_order.price, sell_order.price)
        return (False, None)
     
    def match_orders(self):
        logger.debug('match_orders called')
        trades = []
        for buy_order in self._order_book.buy_orders():
            for sell_order in self._order_book.sell_orders():
                orders_match, trade_price = self.order_matches(buy_order,sell_order)
                if orders_match:
                    logger.debug('match_orders: Matching orders found')
                    trades.append(Trade(buy=buy_order, sell=sell_order,price=trade_price))
                    self._order_book.delete(sell_order)
                    break
        logger.debug('match_orders: %s trades matched' % len(trades))
        for trade in trades:
            self._order_book.delete(trade.buy)
        if trades:
            self._latest_price = trades[0].price
            self._latest_volume = trades[0].buy.quantity
            logger.debug('match_orders: setting _latest_price=%s, _latest_volume=%s' 
                         % (self._latest_price, self._latest_volume))
        return trades
      
    def bid_offer(self):
        """Return bid, offer price
        
        Bid and offer are the prices of the highest current buy and lowest current 
        sell orders. If there are no orders of one type then the last trade price
        is returned instead.
        """
        bid = self._order_book.highest_buy_order()
        offer = self._order_book.lowest_sell_order()
        bid = bid if bid else (offer if offer else self._latest_price)
        offer = offer if offer else (bid if bid else self._latest_price)
        return bid, offer
     
    def last_trade(self):
        return self._latest_price, self._latest_volume
     
    def do_trading(self):
        logger.debug('do_trading called')
#         logging.debug('initial state of order book: %s', self._order_book)
        logging.debug('initial state of order book: %s', str(self._order_book))
        for client_id, client in enumerate(self._clients):
            self.current_client = client_id
            logger.debug('calling client %s' % client_id)
            client(self)
            logging.debug('order book after client %s: \n%s' % (client_id, str(self._order_book)))
        self.current_client = None
        # TODO: do_trading should call match_orders. Need to add a test and review other tests.
     
    def add_client(self,client_callable):
        self._clients.append(client_callable)
                      
    def delete_my_orders(self):
        self._order_book.delete_orders_for_client(self.current_client)
        
def clamp(n, max_n, min_n):
    """return n, limited to the range min_n <= n <= max_n
    
    max_n and min_n can be None, which results in no limit
    """
    if max_n is None and min_n is None:
        return n
    elif max_n is None:
        return max(min_n, n)
    elif min_n is None:
        return min(max_n, n)
    else:
        return max(min(max_n, n), min_n)

def match_order(current_price, buy_price, sell_price):
    match = buy_price is None or sell_price is None or buy_price >= sell_price
    new_price = clamp(current_price, buy_price, sell_price)
    return match, new_price if match else current_price

class TestMatching(unittest.TestCase):
    scenarios = (
                # Current price, buy limit, sell limit, match, new price
                # scenario 1: buy and sell prices, current price below, inside and above the range
                (8.0,            11.0,       9.0,       True,   9.0),
                (10.0,           11.0,       9.0,       True,  10.0),
                (12.0,           11.0,       9.0,       True,  11.0),
                # scenario 2: only a buy price, current price above and below
                (1.0,            9.0,       None,       True,   1.0),
                (10.0,           9.0,       None,       True,   9.0),
                # scenario 3: only a sell price, current price above and below
                (11.0,           None,      10.0,       True,  11.0),
                ( 9.0,           None,      10.0,       True,  10.0),
                # scenario 4: no buy or sell price
                (10.0,           None,      None,       True,  10.0),
                # scenario 5: buy lower than sell, no match
                (10.0,           10.0,      11.0,      False,  10.0),
                 )
    def do_scenario(self, current_price, buy_price, sell_price, expected_match, expected_new_price):
        description = 'Scenario: %s,%s,%s,%s,%s' % (
                            current_price, buy_price, sell_price, expected_match, expected_new_price)
        match, new_price = match_order(current_price, buy_price, sell_price)
        self.assertEqual(match, expected_match, description)
        self.assertEqual(new_price, expected_new_price, description)
    def test_matching_scenarios(self):
        for scenario in self.scenarios:
            self.do_scenario(*scenario)
 
class TestClientFunctions(unittest.TestCase):
    class DummyClient(object):
        def __init__(self):
            self.call_count = 0
        def __call__(self,_):
            self.call_count += 1
    def order_submitting_client(self,exchange):
        exchange.submit_order(Order('buy',1000,10.0))
    def test_do_trading_with_no_clients(self):
        exchange = Exchange()
        exchange.do_trading()
    def test_registered_client_is_called(self):
        exchange = Exchange()
        client = self.DummyClient()
        exchange.add_client(client)
        exchange.do_trading()
        self.assertEqual(client.call_count,1)
    def test_two_clients(self):
        exchange = Exchange()
        client1 = self.DummyClient()
        exchange.add_client(client1)
        client2 = self.DummyClient()
        exchange.add_client(client2)
        exchange.do_trading()
        self.assertEqual(client1.call_count,1)
        self.assertEqual(client2.call_count,1)
    def test_client_can_submit_orders(self):
        exchange = Exchange()
        exchange.add_client(self.order_submitting_client)
        exchange.do_trading()
        self.assertEqual(exchange.order_book(), [Order('buy',1000,10.0)])
    def test_client_can_delete_own_orders(self):
        exchange = Exchange()
        exchange.current_client = 1
        exchange.submit_order(Order('buy',10,1.0))
        exchange.current_client = 2
        exchange.submit_order(Order('sell',10,1.0))
        self.assertEqual(len(exchange.order_book()), 2)
        exchange.delete_my_orders()
        self.assertEqual(exchange.order_book(), [Order('buy',10,1.0)])
     
class TestPriceDerivation(unittest.TestCase):
    def test_no_price(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        bid, offer = exchange.bid_offer()
        self.assertEqual(bid, exchange.OPEN_DEFAULT_PRICE)
        self.assertEqual(offer, exchange.OPEN_DEFAULT_PRICE)
    def test_offer_price_only(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000,10.0)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        bid, offer = exchange.bid_offer()
        self.assertEqual(bid, 10.0)
        self.assertEqual(offer, 10.0)
    def test_bid_price_only(self):
        exchange = Exchange()
        buy_order = Order('buy',1000,10.0)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        bid, offer = exchange.bid_offer()
        self.assertEqual(bid, 10.0)
        self.assertEqual(offer, 10.0)
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
        exchange._latest_price = 1.0
        buy_order = Order('buy',1000,10.0)
        sell_order = Order('sell',1000,9.9)
        exchange.current_client = 1
        exchange.submit_order(buy_order)
        exchange.current_client = 2
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
 
    def test_no_match_for_own_orders(self):
        exchange = Exchange()
        exchange.current_client = 1
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.submit_order(sell_order)
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 0)
    
    def test_match_orders(self):
        exchange = Exchange()
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.current_client = 0
        exchange.submit_order(buy_order)
        exchange.current_client = 1
        exchange.submit_order(sell_order)
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].buy, buy_order)
        self.assertEqual(trades[0].sell, sell_order)
         
    def test_matched_orders_removed_from_order_book(self):
        exchange = Exchange()
        exchange.current_client = 1
        buy_order = Order('buy',1000)
        sell_order = Order('sell',1000)
        exchange.submit_order(buy_order)
        exchange.current_client = 2
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
        exchange.current_client = 1
        exchange.submit_order(buy_order)
        exchange.current_client = 2
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
        exchange.current_client = 1
        exchange.submit_order(buy_order_1)
        exchange.submit_order(buy_order_2)
        exchange.current_client = 2
        exchange.submit_order(sell_order)
        trades = exchange.match_orders()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].buy, buy_order_1)
        self.assertEqual(trades[0].sell, sell_order)
        self.assertEqual(len(exchange.order_book()), 1)
        self.assertEqual(exchange.order_book()[0], buy_order_2)
        
# bid lower than offer - no match
# bid equal to offer - match
# bid higher than offer - match
# multiple buys, highest takes it
# multiple sells, lowest takes it
# can't trade with yourself
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()