import argparse
import logging


class Filter(logging.Filter):
    def filter(self, record):
        return len(record.getMessage().split()) % 2 == 0


file_formatter = logging.Formatter(
    "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
)
file_handler = logging.FileHandler("cache.log", mode="w")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

stream_formatter = logging.Formatter(
    "%(asctime)s\t%(levelname)s\t%(name)s\t%(filename)s\t"
    "%(lineno)d\t%(threadName)s\t%(message)s"
)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(stream_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Реализация двусвязного списка
    со специфическими методами, необходимыми для задачи"""

    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def appendleft(self, node):
        """Добавляет node в начало списка"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def lift_up(self, node):
        """Поднимает node в начало списка"""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.appendleft(node)

    def pop(self):
        """Удаляет последний элемент списка"""
        node = self.tail.prev
        self.tail.prev = node.prev
        node.prev.next = self.tail
        return node


class LRUCache:
    def __init__(self, limit=42):
        logger.info("Start LRUCache init")
        if limit <= 0:
            self.limit = 42
            logger.error(
                "got invalid limit %s<=0. Using default value %s",
                limit,
                self.limit,
            )
        self.limit = limit
        self._cache = {}
        self.linked_list = DoublyLinkedList()
        logger.info("End LRUCache init")

    def get(self, key):
        logger.info("Start LRUCache get('%s')", key)
        if key in self._cache:
            logger.info("Key '%s' is in cache", key)
            node = self._cache[key]
            self.linked_list.lift_up(node)
            logger.info(
                "End LRUCache get('%s') with return '%s'", key, node.value
            )
            return node.value
        logger.info("Key '%s' is not in cache", key)
        logger.info("End LRUCache get('%s') with return None", key)
        return None

    def set(self, key, value):
        logger.info("Start LRUCache set('%s','%s')", key, value)
        if key in self._cache:
            node = self._cache[key]
            logger.info(
                "Key '%s' is already in cache with value '%s'", key, node.value
            )
            node.value = value

            self.linked_list.lift_up(node)
        else:
            logger.info("Key '%s' is not yet in cache", key)
            if len(self._cache) >= self.limit:
                logger.warning(
                    "Cache reached max size (%s)",
                    self.limit,
                )
                node = self.linked_list.pop()
                del self._cache[node.key]
                logger.info(
                    "Deleted key '%s' with value '%s'", node.key, node.value
                )
            else:
                if len(self._cache) >= 0.8 * self.limit:
                    logger.warning(
                        "Cache size %s is close to limit %s",
                        len(self._cache),
                        self.limit,
                    )
                else:
                    logger.info(
                        "Cache size before adding '%s' is %s",
                        key,
                        len(self._cache),
                    )

            node = Node(key, value)
            self.linked_list.appendleft(node)
            self._cache[key] = node
        logger.info("End LRUCache set('%s','%s')", key, value)


def lru_cache_work():
    cache = LRUCache(-100)

    cache = LRUCache(5)

    cache.get("k1")
    cache.set("k1", "val1")
    cache.get("k1")

    cache.set("k2", "val2")
    cache.set("k3", "val3")
    cache.set("k4", "val3")
    cache.set("k5", "val5")
    cache.set("k6", "val6")

    cache.get("k1")
    cache.get("k6")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--to_stdout", action="store_true")
    parser.add_argument("-f", "--with_filter", action="store_true")
    args = parser.parse_args()

    logger.addHandler(file_handler)
    if args.with_filter:
        oddMessagesFilter = Filter()
        stream_handler.addFilter(oddMessagesFilter)
        file_handler.addFilter(oddMessagesFilter)
    if args.to_stdout:
        logger.addHandler(stream_handler)

    lru_cache_work()
