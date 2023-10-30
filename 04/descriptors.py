from collections.abc import Sequence
import math

from custom_errors import (
    InvalidValues,
    InvalidColumnIndicies,
    InvalidRowOffsets,
)


class ValuesDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"_values_descriptor_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    @staticmethod
    def _is_valid(values: Sequence) -> (bool, int):
        """
        Функция проверяет, что все элементы values ненулевые.
        Если найден нулевой элемент, то второй элемент возвращаемого
        кортежа -- индекс нулевого элемента
        """
        for i, value in enumerate(values):
            if (not isinstance(value, (float, int))) or math.isclose(
                value, 0.0
            ):
                return (False, i)
        return (True, -1)

    def __set__(self, obj, values: Sequence):
        if obj is None:
            return None

        is_valid_state, index = ValuesDescriptor._is_valid(values)
        if not is_valid_state:
            raise InvalidValues(index)

        return setattr(obj, self.name, values)

    def __delete__(self, obj):
        delattr(obj, self.name)


class ColumnIndiciesDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"_column_indicies_descriptor_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    @staticmethod
    def _is_valid(column_indicies: Sequence) -> (bool, int):
        """
        Если найден невалидный элемент, то второй элемент возвращаемого
        кортежа -- его индекс
        """
        for i, value in enumerate(column_indicies):
            if not (isinstance(value, int) and 0 <= value):
                return (False, i)
        return (True, -1)

    def __set__(self, obj, column_indicies: Sequence):
        if obj is None:
            return None

        is_valid_state, index = ColumnIndiciesDescriptor._is_valid(
            column_indicies
        )
        if not is_valid_state:
            raise InvalidColumnIndicies(index)

        return setattr(obj, self.name, column_indicies)

    def __delete__(self, obj):
        delattr(obj, self.name)


class RowOffsetsDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"_row_offsets_descriptor_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    @staticmethod
    def _is_valid(row_offsets: Sequence) -> (bool, int):
        """
        Функция проверяет, что все элементы row_offsets являются валидными.
        Если найден невалидный элемент, то второй элемент возвращаемого
        кортежа -- его индекс
        """
        for i, value in enumerate(row_offsets):
            if not (isinstance(value, int) and 0 <= value):
                return (False, i)
        if row_offsets[0] != 0:
            return (False, 0)
        for i in range(1, len((row_offsets))):
            if row_offsets[i] < row_offsets[i - 1]:
                return (False, i)
        return (True, -1)

    def __set__(self, obj, row_offsets: Sequence):
        if obj is None:
            return None

        is_valid_state, index = RowOffsetsDescriptor._is_valid(row_offsets)
        if not is_valid_state:
            raise InvalidRowOffsets(index)

        return setattr(obj, self.name, row_offsets)

    def __delete__(self, obj):
        delattr(obj, self.name)
