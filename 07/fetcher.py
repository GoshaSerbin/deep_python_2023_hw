import argparse
import asyncio
import aiohttp


class Fetcher:
    def __init__(self, file_name: str, limit: int):
        self.file_name = file_name
        self.limit = limit
        self.queue = asyncio.Queue(maxsize=self.limit)

    @staticmethod
    async def fetch_url(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(response.status)

    async def consumer(self):
        while True:
            url = await self.queue.get()
            if url is None:
                await self.queue.put(url)
                return
            await Fetcher.fetch_url(url)

    async def producer(self):
        with open(self.file_name, "r", encoding="UTF-8") as file:
            for url in file:
                await self.queue.put(url)
        await self.queue.put(None)

    async def fetch(self):
        asyncio.create_task(self.producer())

        consumer_tasks = [
            asyncio.create_task(self.consumer()) for _ in range(self.limit)
        ]

        await asyncio.gather(*consumer_tasks)


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--limit", default="1")
parser.add_argument("-f", "--file_name")
args = parser.parse_args()

fetcher = Fetcher(args.file_name, int(args.limit))

asyncio.run(fetcher.fetch())
