from typing import Any
from sources.source_manager import SourceManager
from utils.get_order_from_collection import get_oldest_order_in_collection


class BufferFetchingManager:
    def __init__(self):
        self.__worker_manager = None

    # Singleton
    def __new__(cls) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(BufferFetchingManager, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_order_from_buffer(buffer):
        package_num = BufferFetchingManager.get_highest_prior_package_num(buffer)
        if package_num != -1:
            package = []
            for order in buffer.get_orders():
                if order.get_source_number() == package_num:
                    package.append(order)
            # now we have to decide which order in package has the oldest time_got_buffered
            return get_oldest_order_in_collection(package)
        else:
            return None

    # package number = source number
    @staticmethod
    def get_highest_prior_package_num(buffer):
        if not buffer.is_empty():
            priorities = []

            # get priorities of all the orders in a buffer
            orders = buffer.get_orders()
            for order in orders:
                priorities.append(SourceManager.get_order_priority(order))

            return min(priorities)
        else:
            return -1

    def send_order_to_worker(self, order):
        worker = self.__worker_manager.get_free_worker()
        if worker is not None:
            order.set_time_out_of_buffer(worker.get_time_free())
            worker.process_order(order)

    def set_worker_manager(self, worker_manager):
        self.__worker_manager = worker_manager

    def get_worker_manager(self):
        return self.__worker_manager
