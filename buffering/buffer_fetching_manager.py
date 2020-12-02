from typing import Any
from sources.source_manager import SourceManager
from utils.get_order_from_collection import get_oldest_order_in_collection


class BufferFetchingManager:
    # Singleton
    def __new__(cls) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(BufferFetchingManager, cls).__new__(cls)
        return cls.instance

    # when the order is returned, it is supposed to be removed from the buffer
    @staticmethod
    def get_order_from_buffer(buffer):
        package_num = BufferFetchingManager.get_highest_prior_package_num(buffer)
        if package_num != -1:
            package = []
            for order in buffer.get_orders():
                if order.get_source_number() == package_num:
                    package.append(order)
            # now we have to decide which order in package has the oldest time_got_buffered
            order_to_return = get_oldest_order_in_collection(package)
            buffer.shift_orders(order_to_return.get_pos_in_buffer())
            return order_to_return
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
                print(order.get_time_got_buffered())
                priorities.append(SourceManager.get_order_priority(order))

            return min(priorities)
        else:
            return -1

    @staticmethod
    def send_order_to_worker(order, worker):
        if worker is not None:
            order.set_time_out_of_buffer(worker.get_time_free())
            worker.process_order(order)
        else:
            raise RuntimeError("Logical error! Sending order to worker which is None!")
