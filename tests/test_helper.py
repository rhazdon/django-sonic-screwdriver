from django.http import QueryDict
from django.test import TestCase
from django_sonic_screwdriver.helper import underscoreize


class HelperTest(TestCase):
    def test_underscorize_with_simple_dict(self):
        data = {"test": "test", "ANewTest": "42", 2: "bla"}
        data = underscoreize(data)
        self.assertEqual(data, {2: "bla", "a_new_test": "42", "test": "test"})

    def test_underscorize_with_querydict(self):
        query_dict = QueryDict("AParam=1&AnotherParam=2&c=3")
        data = underscoreize(query_dict)
        self.assertEqual(
            str(data),
            "<QueryDict: {'a_param': ['1'], '_another_param': ['2'], 'c': ['3']}>",
        )
