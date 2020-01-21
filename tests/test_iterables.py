from collections.abc import Iterable

from django.http import QueryDict
from django.test import TestCase
from django_sonic_screwdriver.iterables import get_iterable


class HelperTest(TestCase):
    def test_get_iterable(self):
        data = {"key": "value"}
        self.assertEqual(get_iterable(data), data.items())

        data = QueryDict("AParam=1&AnotherParam=2&c=3")
        self.assertTrue(isinstance(get_iterable(data), Iterable))
