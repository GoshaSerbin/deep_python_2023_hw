import unittest
from unittest import mock

from parse_json import parse_json


class TestParseJson(unittest.TestCase):
    def test_empty_required_fields(self):
        json_str = '{"key1": "word1 word2", "key2": "word3 word4"}'
        required_fields = []
        keywords = ["word2"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = []
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_empty_keywords(self):
        json_str = '{"key1": "word1 word2", "key2": "word3 word4"}'
        required_fields = ["key1", "key2"]
        keywords = []

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = []
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_empty_callback(self):
        json_str = '{"key1": "word1 word2", "key2": "word3 word4"}'
        required_fields = ["key1", "key2"]
        keywords = ["word2"]
        try:
            parse_json(json_str, None, required_fields, keywords)
        except TypeError:
            self.fail("Call a method on None!")

    def test_basic_case(self):
        json_str = '{"key1": "word1 word2", "key2": "word3 word4"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = [mock.call("key1", "word2")]
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_several_keywords(self):
        json_str = '{"key1": "word1 word2 word5", "key2": "word3 word4"}'
        required_fields = ["key1"]
        keywords = ["word1", "word3", "word5"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = [
                mock.call("key1", "word1"),
                mock.call("key1", "word5"),
            ]
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_several_callbacks_with_repeated_word_in_one_field(self):
        json_str = '{"key1": "word1 word1 word1"}'
        required_fields = ["key1"]
        keywords = ["word1"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = [
                mock.call("key1", "word1"),
                mock.call("key1", "word1"),
                mock.call("key1", "word1"),
            ]
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_several_required_fields(self):
        json_str = (
            '{"key1": "word1 word2", "key2": "word3 word4", "key3": "word5'
            ' word6"}'
        )
        required_fields = ["key1", "key3"]
        keywords = ["word1", "word3", "word5"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = [
                mock.call("key1", "word1"),
                mock.call("key3", "word5"),
            ]
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_several_callbacks(self):
        with open("./test_data/test_json.txt", "r", encoding="utf-8") as file:
            json_str = file.read()
            required_fields = ["address", "company", "country", "text"]
            keywords = ["оставить", "ЗАО", "алл."]

            with mock.patch(
                "parse_json.some_keyword_callback"
            ) as callback_mock:
                parse_json(json_str, callback_mock, required_fields, keywords)
            self.assertEqual(3, callback_mock.call_count)

    def test_case_insensitive(self):
        json_str = '{"key1": "WORD1" , "key2": "WoRd2"}'
        required_fields = ["key1", "key2"]
        keywords = ["word1", "wOrD2"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = [
                mock.call("key1", "WORD1"),
                mock.call("key2", "WoRd2"),
            ]
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_matching_several_keywords_in_one_line(self):
        json_str = '{"key1": "word1 word2 word3 word4"}'
        required_fields = ["key1"]
        keywords = ["word1", "word2", "word4"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = [
                mock.call("key1", "word1"),
                mock.call("key1", "word2"),
                mock.call("key1", "word4"),
            ]
            self.assertEqual(expected_calls, callback_mock.mock_calls)

    def test_with_keyword_that_is_not_in_any_of_the_requared_fields(self):
        json_str = (
            '{"key1": "word1 word2", "key2": "word3 word4", "key3": "word5'
            ' word6"}'
        )
        required_fields = ["key1", "key2", "key3"]
        keywords = ["word7"]

        with mock.patch("parse_json.some_keyword_callback") as callback_mock:
            parse_json(json_str, callback_mock, required_fields, keywords)
            expected_calls = []
            self.assertEqual(expected_calls, callback_mock.mock_calls)
