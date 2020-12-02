from buffering.buffer import Buffer
from sources.source_manager import SourceManager
from utils.parse_config import parse_config
from worker.worker_manager import WorkerManager

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

    # все заявки проходят через буфер
    buffer.add_order(order_from_tl)

    # прибор, если свободен, забирает на обслуживание заявку из буфера
    worker_m.notify_buffer_manager(order_from_tl.get_time_in())
