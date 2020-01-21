from django.test import TestCase

from django_sonic_screwdriver.version import version


class VersionTest(TestCase):
    def test_get_version_returns_string(self):
        self.assertIsInstance(version.get_version(), str)