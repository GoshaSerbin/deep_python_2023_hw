import unittest

from CustomList import CustomList


class TestCustomList(unittest.TestCase):
    def test_str_for_empty_list(self):
        actual = str(CustomList([]))
        expected = "[], sum = 0"
        self.assertEqual(actual, expected)

    def test_str_for_basic_list(self):
        actual = str(CustomList([1, 2, 3, 4, 5]))
        expected = "[1, 2, 3, 4, 5], sum = 15"
        self.assertEqual(actual, expected)

    def test_eq_empty_lists(self):
        self.assertTrue(CustomList([]) == CustomList([]))

    def test_eq_lists(self):
        self.assertTrue(CustomList([1, 2, 3, 4, 5]) == CustomList([15]))
        self.assertFalse(CustomList([1, 2]) == CustomList([1]))

    def test_ne_lists(self):
        self.assertTrue(CustomList([1, 2, 3]) != CustomList([1, 2, 3, 4, 5]))
        self.assertFalse(CustomList([0, 5]) != CustomList([5]))

    def test_ge_lists(self):
        self.assertTrue(CustomList([1, 2, 3, 4]) >= CustomList([1, 2]))
        self.assertTrue(CustomList([1, 2]) >= CustomList([1, 2]))
        self.assertFalse(CustomList([1, 2]) >= CustomList([1, 2, 3]))

    def test_gt_lists(self):
        self.assertTrue(CustomList([1, 2, 3, 4]) > CustomList([1, 2]))
        self.assertFalse(CustomList([1, 2]) > CustomList([1, 2]))
        self.assertFalse(CustomList([1, 2]) >= CustomList([1, 2, 3]))

    def test_le_lists(self):
        self.assertFalse(CustomList([1, 2, 3, 4]) <= CustomList([1, 2]))
        self.assertTrue(CustomList([1, 2]) <= CustomList([1, 2]))
        self.assertTrue(CustomList([1, 2]) <= CustomList([1, 2, 3]))

    def test_lt_lists(self):
        self.assertFalse(CustomList([1, 2, 3, 4]) < CustomList([1, 2]))
        self.assertFalse(CustomList([1, 2]) < CustomList([1, 2]))
        self.assertTrue(CustomList([1, 2]) < CustomList([1, 2, 3]))

    def test_add_unequal_custom_lists(self):
        left_list = CustomList([1, 2, 3, 4])
        right_list = CustomList([1, 2, 3, 4, 5, 6])
        lists_sum = left_list + right_list
        self.assertListEqual(list(left_list), [1, 2, 3, 4])
        self.assertListEqual(list(right_list), [1, 2, 3, 4, 5, 6])
        self.assertListEqual(list(lists_sum), [2, 4, 6, 8, 5, 6])

    def test_add_equal_custom_lists(self):
        left_list = CustomList([1, 2, 3, 4])
        right_list = CustomList([0, 1, 0, 1])
        lists_sum = left_list + right_list
        self.assertListEqual(list(left_list), [1, 2, 3, 4])
        self.assertListEqual(list(right_list), [0, 1, 0, 1])
        self.assertListEqual(list(lists_sum), [1, 3, 3, 5])

    def test_sub_unequal_custom_lists(self):
        left_list = CustomList([1, 2, 3, 4])
        right_list = CustomList([1, 2, 3, 4, 5, 6])
        lists_sub = left_list - right_list
        self.assertListEqual(list(left_list), [1, 2, 3, 4])
        self.assertListEqual(list(right_list), [1, 2, 3, 4, 5, 6])
        self.assertListEqual(list(lists_sub), [0, 0, 0, 0, -5, -6])

    def test_sub_equal_custom_lists(self):
        left_list = CustomList([1, 2, 3, 4])
        right_list = CustomList([0, 1, 0, 1])
        lists_sub = left_list - right_list
        self.assertListEqual(list(left_list), [1, 2, 3, 4])
        self.assertListEqual(list(right_list), [0, 1, 0, 1])
        self.assertListEqual(list(lists_sub), [1, 1, 3, 3])

    def test_with_left_list_greater_than_right_list(self):
        left_list = CustomList([1, 2, 3, 4])
        right_list = CustomList([0, 1])
        lists_sub = left_list - right_list
        self.assertListEqual(list(left_list), [1, 2, 3, 4])
        self.assertListEqual(list(right_list), [0, 1])
        self.assertListEqual(list(lists_sub), [1, 1, 3, 4])

    def test_custom_list_add_base_list(self):
        left_list = CustomList([1, 2, 3, 4])
        right_list = [2, 5]
        lists_sum = left_list + right_list
        self.assertListEqual(list(left_list), [1, 2, 3, 4])
        self.assertListEqual(list(right_list), [2, 5])
        self.assertListEqual(list(lists_sum), [3, 7, 3, 4])
        self.assertIsInstance(lists_sum, CustomList)

    def test_base_list_add_custom_list(self):
        left_list = [2, 5]
        right_list = CustomList([1, 2, 3, 4])
        lists_sum = left_list + right_list
        self.assertListEqual(list(left_list), [2, 5])
        self.assertListEqual(list(right_list), [1, 2, 3, 4])
        self.assertListEqual(list(lists_sum), [3, 7, 3, 4])
        self.assertIsInstance(lists_sum, CustomList)

    def test_base_list_sub_custom_list(self):
        left_list = [2, 5]
        right_list = CustomList([1, 2, 3, 4])
        lists_dif = left_list - right_list
        self.assertListEqual(list(left_list), [2, 5])
        self.assertListEqual(list(right_list), [1, 2, 3, 4])
        self.assertListEqual(list(lists_dif), [1, 3, -3, -4])
        self.assertIsInstance(lists_sum, CustomList)
