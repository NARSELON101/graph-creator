import copy
from abc import ABC, abstractmethod
from typing import List

from filterer.base_filter import BaseFilter
from repositories.singleton import Singleton


class BaseFilterer(ABC, Singleton):

    def __init__(self, filters: List[BaseFilter]):
        self.filters = filters

    @abstractmethod
    def filter_data(self, data):
        copied_data = copy.copy(data)
        for filter_obj in self.filters:
            copied_data = filter_obj.run(copied_data)

        return copied_data
