from urllib.request import urlopen
import argparse
import threading
from queue import Queue
import socket
from collections import Counter
import re


HOST_NAME = "localhost"
PORT = 10000
DATA_SIZE = 4096


def find_most_common(text: str, k: int):
    words = re.findall(r"\w+", text)
    return dict(Counter(words).most_common(k))


class Server:
    def __init__(self, thread_num, top_num):
        self.thread_num = int(thread_num)
        self.top_num = int(top_num)
        self.statistic = 0
        self.lock = threading.Lock()
        self.client_sock = socket.socket()
        self.is_working = True

    def work(self, q: Queue):
        while self.is_working:
            url = q.get()
            with urlopen(url) as response:
                the_page = str(response.read())
                self.client_sock.sendall(
                    str(find_most_common(the_page, self.top_num)).encode()
                )
            with self.lock:
                self.statistic += 1
            print(self.statistic)

    def start(self):
        q = Queue()

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST_NAME, PORT))
        server_sock.listen()

        workers = [
            threading.Thread(target=self.work, args=(q,))
            for _ in range(self.thread_num)
        ]

        for worker in workers:
            worker.start()

        while self.is_working:
            self.client_sock, _ = server_sock.accept()

            while True:
                data = self.client_sock.recv(DATA_SIZE)
                if not data:
                    break
                list(map(q.put, data.decode().split()))
            break

        for worker in workers:
            worker.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--thread_num", default="1")
    parser.add_argument("-k", "--top_num", default="1")
    args = parser.parse_args()

    server = Server(args.thread_num, args.top_num)
    server.start()
