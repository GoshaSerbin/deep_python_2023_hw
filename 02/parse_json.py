import json
from typing import Callable


def some_keyword_callback(word: str):
    print(word)


def parse_json(
    json_str: str,
    keyword_callback: Callable,
    required_fields: list[str] = None,
    keywords: list[str] = None,
):
    if required_fields is None or keywords is None:
        return
    json_dict = json.loads(json_str)
    for key, val in json_dict.items():
        if key in required_fields:
            for word in val.split():
                if word in keywords:
                    keyword_callback(word)
