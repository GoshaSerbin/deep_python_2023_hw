import unittest

from custom_errors import (
    InvalidValues,
    InvalidColumnIndicies,
    InvalidRowOffsets,
)

from csr_matrix import CSRMatrix


class TestValuesDescriptor(unittest.TestCase):
    def test_get_attributes(self):
        matrix = CSRMatrix([1, 2, 3], [0, 2, 1], [0, 1, 2])
        # 1 0 0
        # 0 0 2
        # 0 3 0
        self.assertEqual(matrix.values, [1, 2, 3])
        self.assertEqual(matrix.column_indicies, [0, 2, 1])
        self.assertEqual(matrix.row_offsets, [0, 1, 2])

    def test_set_attributes(self):
        matrix = CSRMatrix([1, 2, 3], [0, 2, 1], [0, 1, 2])
        # 1 0 0
        # 0 0 2
        # 0 3 0
        matrix.values = [3, 2, 1]
        matrix.column_indicies = [1, 2, 0]
        matrix.row_offsets = [0, 0, 1]
        # 0 3 2
        # 1 0 0
        # 0 0 0
        self.assertEqual(matrix.values, [3, 2, 1])
        self.assertEqual(matrix.column_indicies, [1, 2, 0])
        self.assertEqual(matrix.row_offsets, [0, 0, 1])

    def test_invalid_arguments_for_values_descriptor(self):
        matrix = CSRMatrix([1, 2, 3], [0, 2, 1], [0, 1, 2])
        # 1 0 0
        # 0 0 2
        # 0 3 0
        self.assertRaises(
            InvalidValues, setattr, matrix, "values", [0, 2, 3]
        )  # must be nonzeros

        self.assertRaises(
            InvalidValues, setattr, matrix, "values", [0.0, 2.0, 3.0]
        )  # must be nonzeros

        self.assertRaises(
            InvalidValues, setattr, matrix, "values", [1, 2, "str"]
        )  # must be float or int

        self.assertRaises(
            InvalidValues, setattr, matrix, "values", [1, 2, (3, 4)]
        )  # must be float or int

        self.assertRaises(
            InvalidValues, setattr, matrix, "values", [1, [2, 5], 3]
        )  # must be float or int

    def test_invalid_arguments_for_column_indicies_descriptor(self):
        matrix = CSRMatrix([1, 2, 3], [0, 2, 1], [0, 1, 2])
        # 1 0 0
        # 0 0 2
        # 0 3 0
        self.assertRaises(
            InvalidColumnIndicies,
            setattr,
            matrix,
            "column_indicies",
            [-1, 1, 2],
        )  # must be non-negative

        self.assertRaises(
            InvalidColumnIndicies,
            setattr,
            matrix,
            "column_indicies",
            [0, "1", 2],
        )  # must be int

        self.assertRaises(
            InvalidColumnIndicies,
            setattr,
            matrix,
            "column_indicies",
            [0, 1, 2.0],
        )  # must be int

    def test_invalid_arguments_for_row_offsets(self):
        matrix = CSRMatrix([1, 2, 3], [0, 2, 1], [0, 1, 2])
        # 1 0 0
        # 0 0 2
        # 0 3 0
        self.assertRaises(
            InvalidRowOffsets, setattr, matrix, "row_offsets", [-1, 1, 2]
        )  # must be non-negative

        self.assertRaises(
            InvalidRowOffsets, setattr, matrix, "row_offsets", [0, 1, 0]
        )  # must not decrease

        self.assertRaises(
            InvalidRowOffsets, setattr, matrix, "row_offsets", [2, 1, 3]
        )  # must not decrease

        self.assertRaises(
            InvalidRowOffsets, setattr, matrix, "row_offsets", [0, "1", 2]
        )  # must be int

        self.assertRaises(
            InvalidRowOffsets, setattr, matrix, "row_offsets", [0, 1, 2.0]
        )  # must be int

    def test_possible_cases(self):
        matrix = CSRMatrix([1, 2, 3], [0, 2, 1], [0, 1, 2])
        # 1 0 0
        # 0 0 2
        # 0 3 0
        matrix.values = (3.3, -2.1, 1, 2, 2, 2)  # int and float

        class MyList(list):  # inheritance from list
            pass

        matrix.column_indicies = MyList([0, 1, 2, 0, 1, 2])
        matrix.row_offsets = MyList([0, 0, 0, 1, 1, 1])
        # 3.3 -2.1  1
        # 2.0  2.0  2.0
        # 0    0    0
        self.assertEqual(matrix.values, (3.3, -2.1, 1, 2.0, 2.0, 2.0))
        self.assertEqual(matrix.column_indicies, MyList([0, 1, 2, 0, 1, 2]))
        self.assertEqual(matrix.row_offsets, MyList([0, 0, 0, 1, 1, 1]))
