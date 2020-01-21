from collections.abc import Iterable

from django.http import QueryDict
from django.test import TestCase
from django_sonic_screwdriver.iterables import count, get_iterable, is_iterable


class IterablesTest(TestCase):
    def test_count(self):
        data = {"key": "value"}
        self.assertEqual(count(data), 1)
        self.assertEqual(count(iter(data)), 1)
        with self.assertRaises(TypeError):
            self.assertEqual(count(1), 0)

    def test_get_iterable(self):
        data = {"key": "value"}
        self.assertEqual(get_iterable(data), data.items())

        data = QueryDict("AParam=1&AnotherParam=2&c=3")
        self.assertTrue(isinstance(get_iterable(data), Iterable))

    def test_is_iterable(self):
        self.assertTrue(is_iterable({}))
        self.assertTrue(is_iterable([]))
        self.assertTrue(is_iterable("a"))
        self.assertFalse(is_iterable(2))

