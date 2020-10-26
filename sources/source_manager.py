from typing import Any

import sources.source as source

class SourceManager:
    def __init__(self, source_amount=1):
        self.__source_amount = source_amount

    # Singleton
    def __new__(cls) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(SourceManager, cls).__new__(cls)
        return cls.instance

    def generate_sources(self):
        sources = []
        for i in range(self.__source_amount):
            s = source.Source
            sources.append(s)
        return sources

    # def get_order_priority(self):