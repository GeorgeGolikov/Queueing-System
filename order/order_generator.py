from order.order import Order
from utils import get_time


def order_generator(source_number, generation_law, delay=0):
    time_generator = get_time.time_next_order(generation_law, delay)
    while True:
        yield Order(source_number, next(time_generator))
