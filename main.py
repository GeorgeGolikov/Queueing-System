from buffering.buffer import Buffer
from buffering.buffer_placement_manager import BufferPlacementManager
from buffering.buffer_fetching_manager import BufferFetchingManager
from order.order import Order
from order.order_generator import order_generator
from sources.source import Source
from sources.source_manager import SourceManager
from utils.get_order_from_collection import get_newest_order_in_collection
from utils.get_order_from_collection import get_oldest_order_in_collection
from utils.get_time import get_time_working
from utils.get_time import time_next_order
from utils.parse_config import parse_config
from worker.worker import Worker
from worker.worker_manager import WorkerManager

import random
import queue

# ==============================
# CREATE BUFFER OBJECTS
# ==============================
buffer = Buffer.get_instance(int(parse_config("Buffer", "volume")))

# ==============================
# CREATE SOURCES OBJECTS
# ==============================
source_amount = int(parse_config("Source", "amount"))
source_m = SourceManager(source_amount)
sources = source_m.generate_sources()

# ==============================
# CREATE WORKERS OBJECTS
# ==============================
worker_m = WorkerManager(int(parse_config("Worker", "amount")))
workers = worker_m.generate_workers()


# Таймлайн - очередь заявок с приоритетом по времени их поступления
# Абстрактное время в СМО
time_line = queue.PriorityQueue()

# положили первые заявки от всех источников в таймлайн
for i in range(source_amount):
    order = sources[i].generate_order()
    print(order.get_time_in())
    time_line.put(order)
print("==========================")

for i in range(int(parse_config("Iterations", "amount"))):
    # выбираем первую заявку на таймлайне
    order_from_tl = time_line.get()

    # кладём следующую заявку от этого источника на таймлайн
    time_line.put(sources[order_from_tl.get_source_number()].generate_order())

    buffer.add_order(order_from_tl)
    # print(buffer.get_orders()[0].get_time_got_buffered())

    worker_m.notify_buffer_manager(order_from_tl.get_time_in())


