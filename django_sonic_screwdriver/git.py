import os
import re
from subprocess import call

from django_sonic_screwdriver.version_handler import VersionHandler


class Git(object):

	@classmethod
	def git_tag(cls, type):
		version = VersionHandler.get_version()

		""" Create always a normal tag """
		# call(['git', 'tag', '-a', 'v'+version, '-m', 'v'+version])

		""" Then create a specific tag, if needed """
		# if type == 'staging':
		#	call(['git', 'tag', '-a', 'staging-v'+version, '-m', 'staging-v'+version])
		#elif type == 'activate':
		#	call(['git', 'tag', '-a', 'activate-v'+version, '-m', 'activate-v'+version])

		call(['git', 'show', 'v'+version])

	@classmethod
	def git_push(cls):
		call(['git', 'push', 'origin', '--tags'])
