from graphs.graph_constructor.diagrams_types import DiagramTypes
from repositories.singleton import Singleton


class GraphConstructor(Singleton):
    def __init__(self):
        self.types = DiagramTypes

    def get_value_by_attr_name(self, enum_attr_name):
        for graph in self.types:
            if graph.name == enum_attr_name:
                return graph

            for sub_graph in graph.value:
                if sub_graph.name == enum_attr_name:
                    return sub_graph

    def get_available_types(self, column_1_type, column_2_type):
        result = []
        for group in self.types:
            if group.value.condition(column_1_type, column_2_type):
                result += list(group.value)

        return result

    def construct_diagram(self, diagram_method_attr_name, *args, **kwargs):
        diagram_construct_method = self.get_value_by_attr_name(diagram_method_attr_name)
        return diagram_construct_method.value.construct(*args, **kwargs)
