from descriptors import (
    ValuesDescriptor,
    ColumnIndiciesDescriptor,
    RowOffsetsDescriptor,
)


class CSRMatrix:
    """
    Класс хранит разреженную матрицу в формате CSR (Compressed Sparse Row).

    Матрица представляется тремя массивами с определенными ограничениями:
    1) values --- массив ненулевых значений разреженной матрицы
    2) column_indicies --- массив индексов столбцов в матрице элементов values
    (т.е. целые неотрицательные числа)
    3) row_offsets --- массив индексов, на i-м месте стоит индекс,
    с которого в values начинается строка i
    (т.е. тоже неотрицательные числа, но идущие в порядке неубывания,
    также первый элемент всегда нулевой)
    """

    values = ValuesDescriptor()
    column_indicies = ColumnIndiciesDescriptor()
    row_offsets = RowOffsetsDescriptor()

    def __init__(self, values, column_indicies, row_offsets):
        self.values = values
        self.column_indicies = column_indicies
        self.row_offsets = row_offsets
