import argparse
import json
import ujson

import cjson


def test_perfomance(file_name: str, repeats_number: int):
    for _ in range(repeats_number):
        with open(file_name, "r", encoding="utf-8") as file:
            json_str = file.read()
        json_dict = json.loads(json_str, parse_int=int, parse_float=float)
        ujson_dict = ujson.loads(json_str)
        cjson_dict = cjson.loads(json_str)
        assert json_dict == cjson_dict == ujson_dict

        json_str = json.dumps(json_dict)
        ujson_str = ujson.dumps(ujson_dict)
        cjson_str = cjson.dumps(cjson_dict)
        assert json_str == cjson_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repeats_number", default=50000)
    args = parser.parse_args()
    test_perfomance("test_data/data.json", args.repeats_number)
