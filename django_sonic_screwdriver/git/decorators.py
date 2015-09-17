from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.utils.shell import Shell


def git_available(func):
	"""

	:param func:
	:return:
	"""
	def inner(self, *args):
		return func(self, *args)

	return inner
