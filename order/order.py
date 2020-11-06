class Order:
    def __init__(self, source_number, time_in):
        self.__source_number = source_number
        self.__time_in = time_in
        self.__time_out = None
        self.__time_got_buffered = None
        self.__time_out_of_buffer = None
        self.__time_service_started = None
        self.__time_service_finished = None

    def get_source_number(self):
        return self.__source_number

    def set_source_number(self, source_number):
        self.__source_number = source_number

    def get_time_in(self):
        return self.__time_in

    def set_time_in(self, time_in):
        self.__time_in = time_in

    def get_time_out(self):
        return self.__time_out

    def set_time_out(self, time_out):
        self.__time_out = time_out

    def get_time_got_buffered(self):
        return self.__time_got_buffered

    def set_time_got_buffered(self, time_got_buffered):
        self.__time_got_buffered = time_got_buffered

    def get_time_out_of_buffer(self):
        return self.__time_out_of_buffer

    def set_time_out_of_buffer(self, time_out_of_buffer):
        self.__time_out_of_buffer = time_out_of_buffer

    def get_time_service_started(self):
        return self.__time_service_started

    def set_time_service_started(self, time_service_started):
        self.__time_service_started = time_service_started

    def get_time_service_finished(self):
        return self.__time_service_finished

    def set_time_service_finished(self, time_service_finished):
        self.__time_service_finished = time_service_finished
