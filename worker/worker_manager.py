from typing import Any
from worker.worker import Worker
from buffering.buffer import Buffer
from buffering.buffer_fetching_manager import BufferFetchingManager
from utils.parse_config import parse_config


class WorkerManager:
    def __init__(self, worker_amount):
        self.__worker_amount = worker_amount
        self.__workers = None
        self.__ptr_worker_pos = 0
        self.__free_workers = None

    # Singleton
    def __new__(cls, worker_amount) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(WorkerManager, cls).__new__(
                cls, worker_amount
            )
        return cls.instance

    def generate_workers(self):
        self.__workers = []
        self.__free_workers = []
        for i in range(self.__worker_amount):
            self.__workers.append(Worker(parse_config("Worker", "service_law"), i, self.__worker_amount, self))
            self.__free_workers.append(True)
        return self.__workers

    # choose device on the ring
    # when the worker is returned, it is supposed that the worker gets busy
    def get_free_worker(self):
        if self.__free_workers[self.__ptr_worker_pos]:
            cur_pos = self.__ptr_worker_pos
            self.__free_workers[cur_pos] = False
            self.__ptr_worker_pos = (self.__ptr_worker_pos + 1) % self.__worker_amount
            return self.__workers[cur_pos]

        cur_pos = (self.__ptr_worker_pos + 1) % self.__worker_amount
        while not self.__free_workers[cur_pos] and \
                cur_pos != self.__ptr_worker_pos:
            cur_pos = (cur_pos + 1) % self.__worker_amount

        if cur_pos != self.__ptr_worker_pos:
            self.__free_workers[cur_pos] = False
            self.__ptr_worker_pos = (cur_pos + 1) % self.__worker_amount
            return self.__workers[cur_pos]
        return None

    def update_free_workers(self, pos, val):
        if isinstance(pos, int) and 0 <= pos < self.__worker_amount and isinstance(val, bool):
            self.__free_workers[pos] = val
        else:
            raise ValueError("Given arguments aren't int and bool or the values are out of bounds")

    def notify_buffer_manager(self):
        worker = self.get_free_worker()
        if worker is not None:
            order = BufferFetchingManager.get_order_from_buffer(Buffer(parse_config("Buffer", "volume")))
            if order is not None:
                BufferFetchingManager.send_order_to_worker(order, worker)
            else:
                raise RuntimeError("Logical error! Buffer does not have any orders!")

    def set_worker_amount(self, worker_amount):
        self.__worker_amount = worker_amount

    def get_worker_amount(self):
        return self.__worker_amount

    def set_workers(self, workers):
        self.__workers = workers

    def get_workers(self):
        return self.__workers

    def set_ptr_worker_pos(self, ptr_worker_pos):
        self.__ptr_worker_pos = ptr_worker_pos

    def get_ptr_worker_pos(self):
        return self.__ptr_worker_pos

    def set_free_workers(self, free_workers):
        self.__free_workers = free_workers

    def get_free_workers(self):
        return self.__free_workers
