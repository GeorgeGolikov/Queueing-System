from order.order import Order
from utils import get_time


class Source:
    def __init__(self, type_, generation_law, number, amount, orders_amount, delay):
        self.__type = type_
        self.__generation_law = generation_law
        self.__number = number
        self.__amount = amount
        self.__orders_amount = orders_amount
        self.__cur_time = 0
        self.__delay = delay

    def generate_order(self, source_number):
        return Order(source_number, get_time.time_next_order(
            self.__generation_law, self.__cur_time, self.__delay
        ))

    def set_type(self, type_):
        self.__type = type_

    def get_type(self):
        return self.__type

    def set_generation_law(self, generation_law):
        self.__generation_law = generation_law

    def get_generation_law(self):
        return self.__generation_law

    def set_number(self, number):
        self.__number = number

    def get_number(self):
        return self.__number

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_orders_amount(self, orders_amount):
        self.__orders_amount = orders_amount

    def get_orders_amount(self):
        return self.__orders_amount

    def set_cur_time(self, cur_time):
        self.__cur_time = cur_time

    def get_cur_time(self):
        return self.__cur_time

    def set_delay(self, delay):
        self.__delay = delay

    def get_delay(self):
        return self.__delay
