import random
import math


def get_time_working(service_law):
    if service_law == "exp":
        return math.exp(random.random())
    else:
        raise ValueError("I can generate time only exponentially!")


def time_next_order(generation_law, cur_time, delay=0):
    if generation_law == "steady":
        return cur_time + delay
