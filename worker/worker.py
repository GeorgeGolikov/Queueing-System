class Worker:
    def __init__(self, service_law, number, amount, manager, busy=False, time_working=0):
        self.__service_law = service_law
        self.__number = number
        self.__amount = amount
        self.__manager = manager
        self.__busy = busy
        self.__time_working = time_working

    def process_order(self, order):

    def notify_free(self):
        self.__manager.update_free_workers(self.__number)

    def set_service_law(self, service_law):
        self.__service_law = service_law

    def get_service_law(self):
        return self.__service_law

    def set_number(self, number):
        self.__number = number

    def get_number(self):
        return self.__number

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_manager(self, manager):
        self.__manager = manager

    def get_manager(self):
        return self.__manager

    def set_busy(self, busy):
        self.__busy = busy

    def is_busy(self):
        return self.__busy

    def set_time_working(self, time_working):
        self.__time_working = time_working

    def get_time_working(self):
        return self.__time_working
