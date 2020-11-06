from typing import Any

class BufferPlacementManager:
    # Singleton
    def __new__(cls) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(BufferPlacementManager, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def find_place_in_buffer():

    @staticmethod
    def find_order_to_reject():
