import unittest
from unittest import mock

from client import Client, HOST_NAME, PORT, DeadPill


class TestClient(unittest.TestCase):
    @mock.patch("builtins.print")
    @mock.patch("client.socket.socket")
    def test_socket_connect_called(self, socket_mock, _):
        client = Client(thread_num=1, file_name="test_data/urls.txt")
        client.start()
        expected = [mock.call((HOST_NAME, PORT))] * 3
        actual = (
            socket_mock.return_value.__enter__.return_value.connect.mock_calls
        )
        self.assertEqual(expected, actual)

    @mock.patch("builtins.print")
    @mock.patch("client.socket.socket")
    @mock.patch("client.Client.add_requests_to_queue")
    def test_producer_task_called_exactly_ones(
        self, producer_task_mock, *_args
    ):
        client = Client(thread_num=1, file_name="test_data/urls.txt")
        client.start()
        self.assertEqual(producer_task_mock.mock_calls, [mock.call()])

    @mock.patch("builtins.print")
    @mock.patch("client.socket.socket")
    @mock.patch("client.Client.send_requests_to_server")
    def test_consumer_tasks_called(self, consumer_task_mock, *_args):
        client = Client(thread_num=1, file_name="test_data/urls.txt")
        client.start()
        consumer_task_mock.assert_called_once_with()

    @mock.patch("builtins.print")
    @mock.patch("client.socket.socket")
    @mock.patch("client.Client.send_requests_to_server")
    def test_consumer_tasks_called_with_many_threads(
        self, consumer_task_mock, *_args
    ):
        client = Client(thread_num=100, file_name="test_data/urls.txt")
        client.start()
        self.assertEqual(
            consumer_task_mock.mock_calls,
            100 * [mock.call()],
        )

    @mock.patch("builtins.print")
    @mock.patch("client.socket.socket")
    def test_queue_only_have_deadpill_when_completed(self, *_args):
        client = Client(thread_num=100, file_name="test_data/urls.txt")
        client.start()
        self.assertEqual(DeadPill, type(client.q.get()))
        self.assertEqual(client.q.qsize(), 0)

    @mock.patch("builtins.print")
    @mock.patch("client.socket.socket")
    def test_client_output(self, socket_mock, print_mock):
        socket_mock.return_value.__enter__.return_value.recv.return_value = (
            b"response"
        )
        client = Client(thread_num=100, file_name="test_data/urls.txt")
        client.start()

        print_mock.assert_has_calls(
            [
                mock.call("link1", ":", "response"),
                mock.call("link2", ":", "response"),
                mock.call("link3", ":", "response"),
            ],
            any_order=True,
        )
