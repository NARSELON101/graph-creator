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
    def convert_df_to_table(self, df_, rows_count):
        pass

    @abstractmethod
    def write_header(self, df_):
        pass

    @abstractmethod
    def write_body(self, df_):
        pass


class HTMLFormatter(BaseFormatter):
    html_table = '<table class="table">' \
                 '{columns}' \
                 '</table>'  # Главный объект (таблица)
    html_body_template = '<tr>{row}</tr>'  # Одна строка
    html_head_template = '<th scope="col">' \
                         '{column_name}' \
                         '</th>'  # Одно значение названия столбца
    html_body_row_template = '<td>{row}</td>'  # Одно значение строки

    df_: DataFrame = None

    def convert_df_to_table(self, df_: DataFrame, rows_count):
        print(df_.dtypes)
        df_ = df_.with_columns([pl.col(column).round(3) for index, column in enumerate(df_.columns) if df_.dtypes[index] in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]])
        with Tag(self.elements, 'table', attributes={"class": "table"}):
            self.write_header(df_)
            self.write_body(df_, count=rows_count)
        return "".join(self.elements)

    def write_header(self, df_):
        with Tag(self.elements, 'thead'):
            with Tag(self.elements, 'tr'):
                for column_name in df_.columns:
                    with Tag(self.elements, 'th'):
                        self.elements.append(column_name)

    def write_body(self, df_, count=1000):
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
