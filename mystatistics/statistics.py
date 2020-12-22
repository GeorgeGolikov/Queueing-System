class Statistics:

    # ==============================
    # PRINT METHODS
    # ==============================

    @staticmethod
    def print_num_of_orders(sources):
        print("========== Numbers of orders")
        for source in sources:
            print("Source", source.get_number(), ": ", source.get_orders_amount())
        print("==========")

    @staticmethod
    def print_reject_probability(sources):
        print("========== Reject probability")
        for source in sources:
            orders_amount = source.get_orders_amount()
            if orders_amount > 0:
                print("Source", source.get_number(), ": ",
                      Statistics.get_num_of_rejected_orders(source) / orders_amount)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were generated")
        print("==========")

    @staticmethod
    def print_average_time_spent_in_system(sources):
        print("========== Average time spent in system")
        for source in sources:
            value = Statistics.get_average_time_spent_in_system(source)
            if value != -1:
                print("Source", source.get_number(), ": ", value)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were generated")
        print("==========")

    @staticmethod
    def print_average_time_spent_in_wait(sources):
        print("========== Average time spent in wait")
        for source in sources:
            value = Statistics.get_average_time_spent_in_wait(source)
            if value != -1:
                print("Source", source.get_number(), ": ", value)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were buffered")
        print("==========")

    @staticmethod
    def print_average_time_spent_in_service(sources):
        print("========== Average time spent in service")
        for source in sources:
            value = Statistics.get_average_time_spent_in_service(source)
            if value != -1:
                print("Source", source.get_number(), ": ", value)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were served")
        print("==========")

    @staticmethod
    def print_worker_use_coef(workers, impl_time):
        if impl_time > 0:
            print("========== Workers use coefficient")
            for worker in workers:
                print("Worker", worker.get_number(), ": ", Statistics.get_worker_use_coef(worker, impl_time))
            print("==========")
        else:
            raise ValueError("Implementation time <= 0!")

    # ==============================
    # GET METHODS
    # ==============================

    @staticmethod
    def get_num_of_rejected_orders(source):
        count = 0
        for order in source.get_orders():
            time_out = order.get_time_out()
            if order.get_time_in() == time_out or time_out == order.get_time_out_of_buffer():
                count += 1
        return count

    @staticmethod
    def get_average_time_spent_in_system(source):
        sum_ = 0
        count_orders = source.get_orders_amount()
        for order in source.get_orders():
            sum_ += order.get_time_out() - order.get_time_in()
        return sum_ / count_orders if count_orders > 0 else -1

    @staticmethod
    def get_average_time_spent_in_wait(source):
        sum_ = 0
        count_orders_buffered = 0
        for order in source.get_orders():
            time_out_of_buffer = order.get_time_out_of_buffer()
            if time_out_of_buffer is not None:
                sum_ += time_out_of_buffer - order.get_time_got_buffered()
                count_orders_buffered += 1
        return sum_ / count_orders_buffered if count_orders_buffered > 0 else -1

    @staticmethod
    def get_average_time_spent_in_service(source):
        sum_ = 0
        count_orders_served = 0
        for order in source.get_orders():
            time_finish = order.get_time_service_finished()
            time_start = order.get_time_service_started()
            if time_finish is not None and time_start is not None:
                sum_ += time_finish - time_start
                count_orders_served += 1
        return sum_ / count_orders_served if count_orders_served > 0 else -1

    @staticmethod
    def get_worker_use_coef(worker, impl_time):
        time_working = worker.get_time_working()
        return time_working / impl_time
