import json
from typing import Callable


def some_keyword_callback(required_field: str, keyword: str):
    print(f"{required_field=}, {keyword=}")


def parse_json(
    json_str: str,
    keyword_callback: Callable,
    required_fields: list[str] = None,
    keywords: list[str] = None,
):
    if required_fields is None or keywords is None or keyword_callback is None:
        return
    json_dict = json.loads(json_str)
    keywords = [keyword.lower() for keyword in keywords]
    for key, val in json_dict.items():
        if key in required_fields:
            for word in val.split():
                if word.lower() in keywords:
                    keyword_callback(key, word)
