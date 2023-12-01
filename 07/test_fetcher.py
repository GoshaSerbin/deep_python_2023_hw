from unittest import IsolatedAsyncioTestCase
from unittest import mock
from unittest.mock import mock_open
import asyncio
from fetcher import Fetcher


async def func():
    await asyncio.sleep(4)


class TestFetcher(IsolatedAsyncioTestCase):
    @mock.patch("fetcher.aiohttp.ClientSession.get")
    async def test_fetch_url(self, get_mock):
        get_mock.return_value.__aenter__.return_value.text.return_value = (
            "word word word other other"
        )
        response = await Fetcher.fetch_url("url")
        self.assertEqual(response, {"word": 3})

    @mock.patch("builtins.print")
    @mock.patch("fetcher.Fetcher.fetch_url")
    async def test_consumer(self, fetch_url_mock, print_mock):
        fetch_url_mock.return_value = "fetch result"
        queue = asyncio.Queue()
        await queue.put("url1")
        await queue.put("url2")
        await queue.put("url3")
        await queue.put(None)

        await Fetcher.consumer(queue)

        fetch_url_expected_calls = [
            mock.call("url1"),
            mock.call("url2"),
            mock.call("url3"),
        ]
        self.assertEqual(fetch_url_expected_calls, fetch_url_mock.mock_calls)

        print_expected_calls = [mock.call("fetch result")] * 3
        self.assertEqual(print_expected_calls, print_mock.mock_calls)

    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="url1\nurl2\nurl3",
    )
    async def test_producer(self, _):
        queue = asyncio.Queue()
        await Fetcher.producer("file", queue)

        self.assertEqual(await queue.get(), "url1")
        self.assertEqual(await queue.get(), "url2")
        self.assertEqual(await queue.get(), "url3")
        self.assertEqual(await queue.get(), None)
        self.assertTrue(queue.empty)

    async def test_fetch_with_different_number_of_workers(self):
        for worker_num in range(1, 100):
            with (
                mock.patch("fetcher.Fetcher.producer") as producer,
                mock.patch("fetcher.Fetcher.consumer") as consumer,
            ):
                fetcher = Fetcher("file", limit=worker_num)
                await fetcher.fetch()
                self.assertEqual(producer.call_count, 1)
                self.assertEqual(consumer.call_count, worker_num)

    async def test_fetch_with_different_number_of_urls_and_workers(self):
        for worker_num in range(1, 10):
            for url_num in range(1, 10):
                with (
                    mock.patch(
                        "fetcher.aiohttp.ClientSession.get"
                    ) as get_mock,
                    mock.patch(
                        "builtins.open",
                        new_callable=mock_open,
                        read_data="url\n" * url_num,
                    ),
                    mock.patch("builtins.print") as print_mock,
                ):
                    get_mock.return_value.__aenter__.return_value.text.return_value = (
                        "word"
                    )

                    fetcher = Fetcher("file", limit=worker_num)
                    await fetcher.fetch()

                    # отправленные запросы

                    get_expected_calls = url_num * [
                        mock.call("url", timeout=1),
                        mock.call().__aenter__(),
                        mock.call().__aenter__().text(),
                        mock.call().__aexit__(None, None, None),
                    ]
                    self.assertEqual(get_expected_calls, get_mock.mock_calls)

                    # полученные ответы
                    print_expected_calls = [mock.call({"word": 1})] * url_num
                    self.assertEqual(
                        print_expected_calls, print_mock.mock_calls
                    )
