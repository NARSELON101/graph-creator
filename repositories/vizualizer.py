import copy
from abc import ABC, abstractmethod

import polars as pl

from repositories.singleton import Singleton
from polars import DataFrame


class Tag:
    """Class for representing an HTML tag."""

    def __init__(self, elements, tag: str, attributes=None) -> None:
        self.tag = tag
        self.elements = elements
        self.attributes = attributes

    def __enter__(self) -> None:
        if self.attributes is not None:
            s = f"<{self.tag} "
            for k, v in self.attributes.items():
                s += f'{k}="{v}" '
            s = f"{s.rstrip()}>"
            self.elements.append(s)
        else:
            self.elements.append(f"<{self.tag}>")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.elements.append(f"</{self.tag}>")


class BaseFormatter(ABC, Singleton):

    def __init__(self):
        self.elements = []

    @abstractmethod
    def convert_df_to_table(self, df_, rows_count, exclude_rows):
        pass

    @abstractmethod
    def write_header(self, df_):
        pass

    @abstractmethod
    def write_body(self, df_):
        pass


class HTMLFormatter(BaseFormatter):
    async def convert_df_to_table(self, df_: DataFrame, rows_count, include_columns):
        all_columns = copy.copy(df_.columns)
        if include_columns:
            print(include_columns, df_.columns)
            for row in copy.copy(df_.columns):
                if row not in include_columns:
                    df_ = df_.drop(row)

        df_ = df_.with_columns([pl.col(column).round(3) for index, column in enumerate(df_.columns) if
                                df_.dtypes[index] in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]])
        with Tag(self.elements, 'table', attributes={"class": "table table-hover"}):
            await self.write_header(df_)
            await self.write_body(df_, count=rows_count)
        return "".join(self.elements), all_columns

    async def write_header(self, df_):
        with Tag(self.elements, 'thead'):
            with Tag(self.elements, 'tr'):
                for column_name in df_.columns:
                    with Tag(self.elements, 'th'):
                        self.elements.append(column_name)

    async def write_body(self, df_, count=1000):
        if count is None:
            filter_func = lambda x: False
        else:
            filter_func = lambda x: x >= count
        with Tag(self.elements, 'tbody'):
            for index, row in enumerate(df_.rows()):

                if filter_func(index):
                    break

                with Tag(self.elements, 'tr'):
                    for val_ in row:
                        with Tag(self.elements, 'td'):
                            if isinstance(val_, float):
                                val_ = round(val_, 3)
                            self.elements.append(str(val_))
