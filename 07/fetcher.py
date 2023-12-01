import argparse
import asyncio
from collections import Counter
import re
import aiohttp


def find_most_common(text: str, k: int):
    words = re.findall(r"\w+", text)
    return dict(Counter(words).most_common(k))


class Fetcher:
    def __init__(self, file_name: str, limit: int):
        self.file_name = file_name
        self.limit = limit

    @staticmethod
    async def fetch_url(url: str, k: int = 1):
        """Функция возвращает словарь k самых популярных слов"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=1) as response:
                return find_most_common(await response.text(), k)

    @staticmethod
    async def consumer(queue: asyncio.Queue):
        while True:
            url = await queue.get()
            if url is None:
                await queue.put(url)
                return
            try:
                answer = await Fetcher.fetch_url(url)
            except asyncio.TimeoutError:
                answer = None
            except aiohttp.ClientConnectorError:
                answer = None
            except Exception:
                answer = None
            print(answer)

    @staticmethod
    async def producer(file_name: str, queue: asyncio.Queue):
        with open(file_name, "r", encoding="UTF-8") as file:
            for url in file:
                await queue.put(url.rstrip())
        await queue.put(None)

    async def fetch(self):
        queue = asyncio.Queue(maxsize=self.limit)
        asyncio.create_task(self.producer(self.file_name, queue))

        consumer_tasks = [
            asyncio.create_task(self.consumer(queue))
            for _ in range(self.limit)
        ]

        await asyncio.gather(*consumer_tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--limit", default="1")
    parser.add_argument("-f", "--file_name")
    args = parser.parse_args()

    fetcher = Fetcher(args.file_name, int(args.limit))

    asyncio.run(fetcher.fetch())
