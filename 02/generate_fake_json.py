#! /usr/bin/env python3

# pip packages
# factory-boy==3.2.1
# Faker==8.8.1
from faker import Faker
import json


def generate_fake_json(file_name: str):
    fake = Faker(locale="Ru_ru")
    with open(file_name, "w", encoding="utf-8") as file:
        data = {
            "name": fake.name(),
            "address": fake.address(),
            "company": fake.company(),
            "country": fake.country(),
            "text": fake.sentence(),
        }
        json.dump(data, file, ensure_ascii=False)


if __name__ == "__main__":
    generate_fake_json("./test_data/test_json.txt")
