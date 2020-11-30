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

# ==============================
# CREATE BUFFER OBJECTS
# ==============================
buffer = Buffer(parse_config("Buffer", "volume"))

# ==============================
# CREATE SOURCES OBJECTS
# ==============================
source_m = SourceManager(parse_config("Source", "amount"))
sources = source_m.generate_sources()

# ==============================
# CREATE WORKERS OBJECTS
# ==============================
worker_m = WorkerManager(parse_config("Worker", "amount"))
workers = worker_m.generate_workers()


for i in range(parse_config("Iterations", "amount")):
    order = random.choice(sources).generate_order()

    buffer.add_order(order)

    worker_m.notify_buffer_manager(order.get_time_in())


