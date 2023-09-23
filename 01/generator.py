from typing import Union, IO


def occurrences_generator(
    file_argument: Union[str, IO], search_words: list[str]
):
    if isinstance(file_argument, str):
        with open(file_argument, "r", encoding="UTF-8", buffering=1) as file:
            for item in inner_generator(file, search_words):
                yield item
    else:
        for item in inner_generator(file_argument, search_words):
            yield item


def inner_generator(file: IO, search_words: list[str]):
    for line in file:
        line_words = line.lower().split()
        for word in search_words:
            if word.lower() in line_words:
                yield line.rstrip("\n")
                break
