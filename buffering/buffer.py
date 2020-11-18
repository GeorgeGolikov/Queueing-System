from typing import Any
from utils.get_cur_time import get_current_time
from order.order import Order
from buffering.buffer_placement_manager import BufferPlacementManager


class Buffer:
    def __init__(self, volume):
        self.__volume = volume
        self.__orders = [None] * volume
        self.__orders_amount_now = 0
        self.__rejected_orders_amount = 0

    # Singleton
    def __new__(cls, volume) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Buffer, cls).__new__(cls, volume)
        return cls.instance

    def set_volume(self, volume):
        self.__volume = volume

    def get_volume(self):
        return self.__volume

    def get_orders(self):
        return self.__orders

    def get_orders_amount_now(self):
        return self.__orders_amount_now

    def get_rejected_orders_amount(self):
        return self.__rejected_orders_amount

    def is_empty(self):
        return self.__orders_amount_now == 0

    def is_full(self):
        return self.__orders_amount_now == self.__volume

    def reject_order(self, pos):
        if isinstance(pos, int) and 0 <= pos < self.__volume:
            cur_time = get_current_time()
            self.__orders[pos].set_time_out(cur_time)
            self.__orders[pos].set_time_out_of_buffer(cur_time)
            self.shift_orders(pos)
            self.__rejected_orders_amount += 1
            self.__orders_amount_now -= 1
        else:
            raise IndexError

    def shift_orders(self, pos):
        ord_am = self.__orders_amount_now
        if isinstance(pos, int) and 0 <= pos < ord_am:
            for i in range(pos, ord_am - 1):
                self.__orders[i] = self.__orders[i+1]
            self.__orders[ord_am - 1] = None
        else:
            raise IndexError

    def add_order(self, order):
        if isinstance(order, Order):
            pos = BufferPlacementManager.find_place_in_buffer(self)
            if pos is not None:
                self.__orders[pos] = order
            else:
                pos_reject = BufferPlacementManager.find_order_to_reject(self, order)
                if pos_reject is not None:
                    self.reject_order(pos_reject)
                    self.__orders[self.__orders_amount_now] = order
                else:
                    order.set_time_out(get_current_time())
                    self.__rejected_orders_amount += 1
        else:
            raise TypeError("Given argument is not Order type!")
