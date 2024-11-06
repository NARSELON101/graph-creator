from abc import ABC, abstractmethod

from polars import DataFrame


class BaseFilter(ABC):

    @abstractmethod
    def run(self, data):
        pass


class BaseDataFrameFilter(BaseFilter):

    @abstractmethod
    def run(self, data: DataFrame):
        pass
