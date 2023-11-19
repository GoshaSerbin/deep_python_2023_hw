import unittest

from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_set_and_get_key(self):
        cache = LRUCache(10)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

    def test_default_value(self):
        cache = LRUCache(10)
        self.assertIs(cache.get("k1"), None)
        self.assertIs(cache.get("k2"), None)
        self.assertIs(cache.get("k3"), None)

    def test_reseting_value(self):
        cache = LRUCache(10)
        self.assertIs(cache.get("k1"), None)
        cache.set("k1", "val1")
        self.assertEqual(cache.get("k1"), "val1")
        cache.set("k1", "new_val1")
        self.assertEqual(cache.get("k1"), "new_val1")

    def test_cache_size_limitation(self):
        cache = LRUCache(3)

        self.assertIs(cache.get("k1"), None)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        cache.set("k4", "val4")

        self.assertIs(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k4"), "val4")

    def test_reuse_keys(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        cache.get("k1")
        cache.set("k1", "new_val1")
        cache.get("k1")

        cache.set("k3", "val3")

        self.assertIs(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "new_val1")
        self.assertEqual(cache.get("k3"), "val3")

    def test_case_like_in_task(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

    def test_with_cache_size_eq_1(self):
        cache = LRUCache(1)

        cache.set("k1", "val1")
        self.assertEqual(cache.get("k1"), "val1")
        cache.set("k2", "val2")
        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k3"), "val3")

    def test_changing_existing_key_and_consequences(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k1", "new_val1")
        cache.set("k3", "val3")

        self.assertEqual(cache.get("k1"), "new_val1")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k3"), "val3")
