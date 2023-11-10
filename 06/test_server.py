import unittest
from unittest import mock

from server import Server, DeadPill


class TestServer(unittest.TestCase):
    @mock.patch("server.urllib.request.urlopen")
    @mock.patch("builtins.print")
    @mock.patch("server.socket.socket")
    def test_socket_accept_called(self, server_sock_mock, *_args):
        client_sock_mock = mock.MagicMock()
        server_sock_mock.return_value.accept.return_value = (
            client_sock_mock,
            1,
        )
        server = Server(thread_num=1)
        server.is_working = mock.Mock(side_effect=[True, False])
        server.start()
        server_sock_mock.return_value.accept.assert_called_once_with()

    @mock.patch("server.urllib.request.urlopen")
    @mock.patch("builtins.print")
    @mock.patch("server.Server.work")
    @mock.patch("server.socket.socket")
    def test_work_tasks_called(self, server_sock_mock, work_mock, *_args):
        client_sock_mock = mock.MagicMock()
        server_sock_mock.return_value.accept.return_value = (
            client_sock_mock,
            1,
        )
        server = Server(thread_num=1)
        server.is_working = mock.Mock(side_effect=[True, False])
        server.start()
        work_mock.assert_called_once_with()

    @mock.patch("server.urllib.request.urlopen")
    @mock.patch("builtins.print")
    @mock.patch("server.Server.work")
    @mock.patch("server.socket.socket")
    def test_work_tasks_called_with_many_threads(
        self, server_sock_mock, work_mock, *_args
    ):
        client_sock_mock = mock.MagicMock()
        server_sock_mock.return_value.accept.return_value = (
            client_sock_mock,
            1,
        )
        server = Server(thread_num=100)
        server.is_working = mock.Mock(side_effect=[True, False])
        server.start()
        self.assertEqual(
            work_mock.mock_calls,
            100 * [mock.call()],
        )

    @mock.patch("builtins.print")
    @mock.patch("server.urlopen")
    @mock.patch("server.socket.socket")
    def test_urlopen_called(self, server_sock_mock, urlopen_mock, *_args):
        client_sock_mock = mock.Mock()
        client_sock_mock.recv.return_value = b"link"
        server_sock_mock.return_value.accept.return_value = (
            client_sock_mock,
            1,
        )
        server = Server(thread_num=1)
        server.is_working = mock.Mock(side_effect=[True, False])
        server.start()
        self.assertIn(mock.call("link", timeout=1.0), urlopen_mock.mock_calls)

    @mock.patch("builtins.print")
    @mock.patch("server.urlopen")
    @mock.patch("server.socket.socket")
    def test_statistic(self, server_sock_mock, *_args):
        client_sock_mock = mock.Mock()
        client_sock_mock.recv.return_value = b"link"
        server_sock_mock.return_value.accept.return_value = (
            client_sock_mock,
            1,
        )
        server = Server(thread_num=100)

        server.is_working = mock.Mock(side_effect=50 * [True] + [False])
        server.start()
        self.assertEqual(server.statistic, 50)

    @mock.patch("builtins.print")
    @mock.patch("server.urlopen")
    @mock.patch("server.socket.socket")
    def test_queue_only_have_deadpill_when_completed(
        self, server_sock_mock, *_args
    ):
        client_sock_mock = mock.Mock()
        client_sock_mock.recv.return_value = b"link"
        server_sock_mock.return_value.accept.return_value = (
            client_sock_mock,
            1,
        )
        server = Server(thread_num=100)

        server.is_working = mock.Mock(side_effect=50 * [True] + [False])
        server.start()
        self.assertEqual(DeadPill, type(server.q.get()))
        self.assertEqual(server.q.qsize(), 0)
