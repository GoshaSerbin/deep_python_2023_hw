import unittest
from unittest import mock

from mean_decorator import mean, InvalidArguments


class TestMeanDecorator(unittest.TestCase):
    def test_invalid_arguments(self):
        self.assertRaises(InvalidArguments, mean, 0)

    @mock.patch("builtins.print")
    @mock.patch("mean_decorator.time.time")
    def test_basic_case(self, time_mock, print_mock):
        calls_number = 100
        time_mock.side_effect = [
            0 if i % 2 == 0 else 1 for i in range(2 * calls_number)
        ]

        @mean(50)
        def empty_func():
            pass

        for _ in range(calls_number):
            empty_func()

        self.assertEqual(
            [mock.call("1.0")] * calls_number, print_mock.mock_calls
        )
