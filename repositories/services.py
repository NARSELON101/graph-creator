import os

from polars.exceptions import ComputeError
from polars.datatypes import IntegerType
import polars as pl

separators = [',', '\t', '\n']


def get_dataframe_from_path(graph_path) -> tuple[pl.DataFrame, list[str]]:
    pl_ = pl.DataFrame()
    for sep in separators:
        try:
            pl_ = pl.read_csv(str(graph_path), separator=sep)
            if len(pl_.columns) == 1:
                continue
            else:
                return pl_, pl_.columns

        except ComputeError:
            pass

    return pl_, pl_.columns


def get_df_column_values(graph, columns: list = None):
    result = []
    if graph and columns:
        df_, _ = get_dataframe_from_path(graph.path)
        if columns is None:
            columns = []

        for col in columns:
            result.append(df_.get_column(col).to_list())

    return result


def get_column_type(column_values):
    result = []

    for val in column_values:
        if isinstance(val, str):
            result.append(not val.isdigit())
        else:
            return int
    return str if all(result) else int


def handle_uploaded_file(file, user, title, model):
    file_path = f'/{user.id}/{file}'
    if not os.path.exists(f'graph_storage/{user.id}'):
        os.mkdir(f'graph_storage/{user.id}/')
    with open(f"graph_storage{file_path}", "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    df_data = get_dataframe_from_path(f'graph_storage{file_path}')
    columns = df_data[1]
    data_types = df_data[0].dtypes
    data = []
    for data_type, col in zip(data_types, columns):
        col_type = data_type.to_python()
        col_type = 'digit' if col_type in [int, float] else 'string'
        if col:
            data.append({"name": col, 'type': col_type})

    columns_data = {"columns": data}

    graph, is_created = model.objects.get_or_create(path=f"graph_storage{file_path}",
                                                    user=user,
                                                    name=title,
                                                    columns=columns_data)
    return is_created
