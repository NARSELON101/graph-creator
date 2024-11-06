import copy
from typing import List

from filterer.base import BaseFilterer
from filterer.base_filter import BaseFilter
from polars import DataFrame


class DataFrameFilter(BaseFilterer):

    def __init__(self, filters: List[BaseFilter]):
        super().__init__(filters=filters)

    async def filter_data(self, data: DataFrame):
        copied_data = copy.copy(data)
        for filter_obj in self.filters:
            copied_data = filter_obj.run(copied_data)
        return copied_data
