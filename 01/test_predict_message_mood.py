import unittest
from unittest.mock import Mock

from predict_message_mood import (
    predict_message_mood,
    SomeModel,
    InvalidArguments,
)


class TestPredictMessageMood(unittest.TestCase):
    def test_boundary_case_for_bad_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.3

        self.assertEqual("норм", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_boundary_case_for_good_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.8

        self.assertEqual("норм", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_with_value_little_over_good_threshold(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.800001

        self.assertEqual("отл", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_with_value_slightly_less_than_good_threshold(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.79999999

        self.assertEqual("норм", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_with_value_little_over_bad_threshold(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.300001

        self.assertEqual("норм", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_with_value_slightly_less_than_bad_threshold(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.29999999

        self.assertEqual("неуд", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_predict_bad_mood_with_default_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0

        self.assertEqual("неуд", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_predict_good_mood_with_default_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 1

        self.assertEqual("отл", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_predict_normal_mood_with_default_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.5

        self.assertEqual("норм", predict_message_mood("msg", mock_model))
        mock_model.predict.assert_called_with("msg")

    def test_predict_bad_mood_with_specific_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 0

        self.assertEqual(
            "неуд",
            predict_message_mood(
                "msg", mock_model, bad_thresholds=1, good_thresholds=2
            ),
        )
        mock_model.predict.assert_called_with("msg")

    def test_predict_good_mood_with_specific_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 3

        self.assertEqual(
            "отл",
            predict_message_mood(
                "msg", mock_model, bad_thresholds=1, good_thresholds=2
            ),
        )
        mock_model.predict.assert_called_with("msg")

    def test_predict_normal_mood_with_specific_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        mock_model.predict.return_value = 1.5

        self.assertEqual(
            "норм",
            predict_message_mood(
                "msg", mock_model, bad_thresholds=1, good_thresholds=2
            ),
        )
        mock_model.predict.assert_called_with("msg")

    def test_invalid_thresholds(self):
        mock_model = Mock(spec=SomeModel)
        self.assertRaises(
            InvalidArguments,
            predict_message_mood,
            "msg",
            mock_model,
            bad_thresholds=1,
            good_thresholds=0,
        )
