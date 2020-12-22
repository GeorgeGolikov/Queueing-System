from buffering.buffer import Buffer
from sources.source_manager import SourceManager
from utils.parse_config import parse_config
from worker.worker_manager import WorkerManager
from mystatistics.statistics import Statistics

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
while not(time_line.empty()):
    order_from_tl = time_line.get()
    buffer.add_order(order_from_tl)
    worker_m.notify_buffer_manager(order_from_tl.get_time_in())

# конец реализации - время освобождения последнего прибора
last_times_free = []
for worker in workers:
    last_times_free.append(worker.get_time_free())
time_impl_end = max(last_times_free)

# заявки, оставшиеся в буфер к концу реализации, идут в отказ
while not(buffer.is_empty()):
    buffer.reject_order(0, time_impl_end)

# ==============================
# ВЫВОД СТАТИСТИКИ. РЕЖИМ АВТО
# ==============================
Statistics.print_num_of_orders(sources)
Statistics.print_reject_probability(sources)
Statistics.print_average_time_spent_in_system(sources)
Statistics.print_average_time_spent_in_wait(sources)
Statistics.print_average_time_spent_in_service(sources)
Statistics.print_worker_use_coef(workers, time_impl_end)

# index = 2
# print(sources[index].get_orders_amount())
# count_orders_buffered = 0
# count_orders_rejected = 0
# for order in sources[index].get_orders():
#     time_out_of_buffer = order.get_time_out_of_buffer()
#     if time_out_of_buffer is not None:
#         count_orders_buffered += 1
#     if order.get_time_in() == order.get_time_out():
#         count_orders_rejected += 1
# print(count_orders_buffered)
# print(count_orders_rejected)
