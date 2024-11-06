from graphs.graph_constructor.construct_methods import LinearConstructMethod, ScatterConstructMethod
from graphs.types import Choice


class DigitDiagram(Choice):
    """ Тип диаграмм, где X и Y - целочисленные значения """
    aboba = LinearConstructMethod(), 'Линия'
    aboba1 = ScatterConstructMethod(), 'Точка'

    @staticmethod
    def condition(x_type, y_type):
        return (issubclass(x_type, int) and issubclass(y_type, int)) is True


class StrAndDigitDiagram(Choice):
    """ Тип диаграмм, где X или Y - строчное значение, а другой - целочисленный """
    bar_chart = "func()", "Столбчатая диаграмма"
    histogram = "func", "Гистограмма"
    scatter_plot = 'func', 'Диаграмма разброса'

    @staticmethod
    def condition(x_type, y_type):
        return ((issubclass(x_type, int) and issubclass(y_type, str)) or
                (issubclass(x_type, str) and issubclass(y_type, int))) is True


class DiagramTypes(Choice):
    str_and_digit = StrAndDigitDiagram
    digits_diagrams = DigitDiagram
