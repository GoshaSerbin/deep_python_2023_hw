from urllib.request import urlopen
import argparse
import threading
from queue import Queue
import socket
from collections import Counter
import re
import urllib


HOST_NAME = "localhost"
PORT = 10000
DATA_SIZE = 4096


class DeadPill:
    pass


def find_most_common(text: str, k: int):
    words = re.findall(r"\w+", text)
    return dict(Counter(words).most_common(k))


class Server:
    def __init__(self, thread_num, top_num=1):
        self.thread_num = int(thread_num)
        self.top_num = int(top_num)
        self.statistic = 0
        self.lock = threading.Lock()
        self.q = Queue()

    def is_working(self):
        return True

    def work(self):
        while True:
            task = self.q.get()

            if isinstance(task, DeadPill):
                self.q.put(task)
                return

            url, client_sock = task

            try:
                with urlopen(url, timeout=1.0) as response:
                    the_page = str(response.read())
                    answer = str(find_most_common(the_page, self.top_num))
            except urllib.error.URLError:
                answer = "URL error."
            except UnicodeDecodeError:
                answer = "URL error."
            except TimeoutError:
                answer = "Timeout error"

            client_sock.sendall(answer.encode())

            with self.lock:
                self.statistic += 1
            print(self.statistic)

    def start(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST_NAME, PORT))
        server_sock.listen()

        workers = [
            threading.Thread(target=self.work) for _ in range(self.thread_num)
        ]

        for worker in workers:
            worker.start()

        server_sock.settimeout(15.0)

        while self.is_working():
            try:
                client_sock, _ = server_sock.accept()
            except TimeoutError:
                break

            data = client_sock.recv(DATA_SIZE)
            if not data:
                break
            self.q.put((data.decode(), client_sock))
        client_sock.close()

        self.q.put(DeadPill())
        for worker in workers:
            worker.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--thread_num", default="1")
    parser.add_argument("-k", "--top_num", default="1")
    args = parser.parse_args()

    server = Server(args.thread_num, args.top_num)
    server.start()
