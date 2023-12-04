import argparse
import threading
from queue import Queue
import socket


class DeadPill:
    pass


HOST_NAME = "localhost"
PORT = 10000
DATA_SIZE = 4096


class Client:
    def __init__(self, thread_num: int, file_name: str):
        self.thread_num = int(thread_num)
        self.file_name = file_name
        self.q = Queue(maxsize=self.thread_num)

    def add_requests_to_queue(self):
        with open(self.file_name, "r", encoding="UTF-8") as file:
            for url in file:
                self.q.put(url)

    def send_requests_to_server(self):
        while True:
            url = self.q.get()
            if isinstance(url, DeadPill):
                self.q.put(url)
                return
            try:
                with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                ) as client_sock:
                    client_sock.connect((HOST_NAME, PORT))
                    client_sock.send(url.encode())
                    data = client_sock.recv(DATA_SIZE)
                    print(url.strip(), ":", data.decode())
            except Exception as e:
                print(e)

    def start(self):
        producer = threading.Thread(target=self.add_requests_to_queue)
        producer.start()

        consumers = [
            threading.Thread(target=self.send_requests_to_server)
            for _ in range(self.thread_num)
        ]
        for consumer in consumers:
            consumer.start()

        producer.join()
        self.q.put(DeadPill())

        for consumer in consumers:
            consumer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--thread_num", default="1")
    parser.add_argument("-f", "--file_name", required=True)
    args = parser.parse_args()

    client = Client(args.thread_num, args.file_name)
    client.start()
