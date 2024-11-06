from enum import Enum
import typing


class Choice(Enum):
    """ Обеспечивает реализацию структур выбора

    Функционально повторяет built-in Enum реализацию, но
    добавляет возможность дополнительно (опционально) указывать название (`label`)
    объекта выбора, а также обеспечивает корректное обновление данных в json схеме операций
    """

    __label_by_name__: bool = False

    def __new__(cls, value, label: str = None):
        field = object.__new__(cls)
        field._value_ = value
        field.label = label
        return field

    @classmethod
    def _get_default_label(cls, field):
        return field.name if cls.__label_by_name__ else str(field.value)

    @classmethod
    def from_enum(cls, enum: typing.Type[Enum], alias: str = None, by_name: bool = False):
        """ Возвращает новый класс структуры выбора на базе существующего класса Enum

        Args:
            enum (Type[_Enum]): Существующий класс типа Enum
            alias (str, optional): Название нового создаваемого класса.
                                   Если не задано - то по умолчанию будет наследовано название передаваемого Enum.
            by_name(bool, optional): Флаг использования названия перечисления в качестве ключа выбора.
                                     По умолчанию имеет значение False - в качестве ключа выступают сами значения.

        Returns:
            Новый класс структуры выбора Choice
        """

        choice = Choice(alias or enum.__name__, {field.name: field.value for field in list(enum)})
        choice.__label_by_name__ = by_name
        return choice

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.pop('title', None)
        field_schema.pop('description', None)
        field_schema.pop('enum', None)

        field_schema.update({
            "choices": {field.label or cls._get_default_label(field): field.value for field in cls}
        })