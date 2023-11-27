import unittest
import json

import cjson


class TestCJSON(unittest.TestCase):
    def test_case_like_in_task(self):
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str, parse_int=int, parse_float=float)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json.dumps(json_doc), cjson.dumps(cjson_doc))

    def test_empty_json(self):
        json_str = "{}"
        json_doc = json.loads(json_str, parse_int=int, parse_float=float)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json.dumps(json_doc), cjson.dumps(cjson_doc))

    def test_single_value(self):
        json_str = '{"field": "val"}'
        json_doc = json.loads(json_str, parse_int=int, parse_float=float)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json.dumps(json_doc), cjson.dumps(cjson_doc))

    def test_numbers(self):
        json_str = (
            '{"f1": 1, "f2": -100, "f3": 10.5, "f4": 1e-3, "f5": -123e+2}'
        )
        json_doc = json.loads(json_str, parse_int=int, parse_float=float)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, cjson_doc)

    def test_strings(self):
        json_str = '{"f1": "hello", "f2": "-100", "f3": ""}'
        json_doc = json.loads(json_str, parse_int=int, parse_float=float)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json.dumps(json_doc), cjson.dumps(cjson_doc))

    def test_string_with_spaces(self):
        json_str = '   {   "f1"   :   "hello"   ,  "f2"   : "-100"  }    '
        json_doc = json.loads(json_str, parse_int=int, parse_float=float)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json.dumps(json_doc), cjson.dumps(cjson_doc))
