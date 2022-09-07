from collections import deque
from sortedcontainers import SortedList
import threading


class Order:

    def __init__(self, id, order_type, side, price, quantity):
        self.id = id
        self.type = order_type
        self.side = side.lower()
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return "[" + str(self.price) + " for " + str(self.quantity) + " shares]"

class Trade:

    def __init__(self, buyer, seller, price, quantity):
        self.buy_order_id = buyer
        self.sell_order_id = seller
        self.price = price
        self.quantity = quantity

    def show(self):
        print("[", self.price, self.quantity, "]")

class OrderBook:

    def __init__(self, bids=[], asks=[]):
        self.bids = SortedList(bids, key = lambda order: -order.price)
        self.asks = SortedList(asks, key = lambda order: order.price)

    def __len__(self):
        return len(self.bids) + len(self.asks)

    def best_bid(self):
        if len(self.bids) > 0:
            return self.bids[0].price
        else:
            return 0

    def best_ask(self):
        if len(self.asks) > 0:
            return self.asks[0].price
        else:
            return 0

    def add(self, order):
        if order.side == 'buy':
            index = self.bids.bisect_right(order)
            self.bids.insert(index, order)
        elif order.side == 'sell':
            index = self.asks.bisect_right(order)
            self.asks.insert(index, order)

    def remove(self, order):
        if order.side == 'buy':
            self.bids.remove(order)
        elif order.side == 'sell':
            self.asks.remove(order)