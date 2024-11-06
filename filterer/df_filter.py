from polars import DataFrame

from filterer.base_filter import BaseDataFrameFilter


class ColumnsFilter(BaseDataFrameFilter):

    def __init__(self, columns):
        self.columns = columns

    def run(self, data: DataFrame):
        if self.columns:
            for row in data.columns:
                if row not in self.columns:
                    data = data.drop(row)

        return data


class RowsCountFilter(BaseDataFrameFilter):

    def __init__(self, rows_count):
        self.rows_count: None | int = rows_count

    def run(self, data: DataFrame):
        if self.rows_count is not None:
            return data.head(self.rows_count)
        return data
