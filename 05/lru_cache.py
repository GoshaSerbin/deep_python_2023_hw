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
        self.limit = limit
        self._cache = {}
        self.linked_list = DoublyLinkedList()

    def get(self, key):
        if key in self._cache:
            node = self._cache[key]
            self.linked_list.lift_up(node)
            return node.value
        return None

    def set(self, key, value):
        if key in self._cache:
            node = self._cache[key]
            node.value = value
            self.linked_list.lift_up(node)
        else:
            if len(self._cache) >= self.limit:
                node = self.linked_list.pop()
                del self._cache[node.key]
            node = Node(key, value)
            self.linked_list.appendleft(node)
            self._cache[key] = node
