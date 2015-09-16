from subprocess import call

from django_sonic_screwdriver.version_handler import VersionHandler
from django_sonic_screwdriver.shell import Shell


GIT_OPTIONS = {
	'DEVELOPMENT': 'development',
	'STAGING': 'staging',
	'PRODUCTION': 'production',
}


class Git(object):

	@classmethod
	def is_enabled(cls):
		if not call(['git', 'rev-parse']):
			return True
		print(Shell.WARNING + 'There is no git repository!' + Shell.ENDC)
		return False

	@classmethod
	def branch_create(cls):
		pass

	@classmethod
	def branch_commit(cls):
		pass

	@classmethod
	def branch_push(cls):
		pass

	@classmethod
	def tag_create(cls, tag=''):
		if cls.is_enabled():
			version = VersionHandler.get_version()

			if tag != '':
				tag += '-'

			print(Shell.OKBLUE + 'Tag version ' + tag + 'v' + version + Shell.ENDC)
			call(['git', 'tag', '-a', tag + 'v' + version, '-m', '\'' + tag + 'v' + version + '\''])

		""" Then create a specific tag, if needed """
		# if type == 'staging':
		#	call(['git', 'tag', '-a', 'staging-v'+version, '-m', 'staging-v'+version])
		#elif type == 'activate':
		#	call(['git', 'tag', '-a', 'activate-v'+version, '-m', 'activate-v'+version])

		# call(['git', 'show', 'v'+version])

	@classmethod
	def tag_delete(cls):
		if cls.is_enabled():
			pass

	@classmethod
	def tag_push(cls):
		pass
		# call(['git', 'push', 'origin', '--tags'])
