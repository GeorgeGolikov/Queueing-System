from typing import Any


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
            self.__orders[pos] = None
            self.__rejected_orders_amount += 1
            self.__orders_amount_now -= 1
        else:
            raise IndexError
