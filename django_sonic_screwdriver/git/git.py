from subprocess import call, check_output

from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.version import Version
from django_sonic_screwdriver.utils import Shell
from django_sonic_screwdriver.git.decorators import git_available


GIT_OPTIONS = {
	'DEVELOPMENT': 'development',
	'STAGING': 'staging',
	'PRODUCTION': 'production',
}


class Git(object):

	@staticmethod
	def is_enabled():
		if not call(['git', 'rev-parse']):
			return True
		Shell.fail('There is no git repository!')
		return exit(1)

	@staticmethod
	def create_git_version_tag(deploy_tag):
		if deploy_tag != '':
				deploy_tag += '-'
		return str(deploy_tag + 'v' + Version.get_version())

	"""
	Basic Git Commands
	"""
	@staticmethod
	def git_add():
		"""
		Add files to staging.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Adding files...')
		if not call(['git', 'add', '-A']):
			return True
		return False

	@staticmethod
	def git_commit(git_tag):
		"""
		Commit files to branch.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Commit changes.')
		if not call(['git', 'commit', '-m', '\'' + git_tag + '\'']):
			return True
		return False

	@staticmethod
	def git_tag(git_tag):
		"""
		Create new tag.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Create tag from version ' + git_tag)
		if not call(['git', 'tag', '-a', git_tag, '-m', '\'' + git_tag + '\'']):
			return True
		return False

	@staticmethod
	def git_tag_gpg(git_tag):
		"""
		Create new tag with GPG signature.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Create signed tag version ' + git_tag + ' with GPG')
		if not call(['git', 'tag', '-s', git_tag, '-m', '\'' + git_tag + '\'']):
			return True
		return False

	"""
	Branch Handling
	"""
	@staticmethod
	def get_current_branch():
		current_branch = str(check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']))
		return current_branch[2:][:(current_branch.__len__()-5)]

	def branch_create(self):
		"""
		Create new branch.
		"""
		# TODO:
		pass

	def branch_push(self):
		branch = self.get_current_branch()

		Shell.msg('Pushing branch ' + branch + ' to server...')
		if not call(['git', 'push', '-u', 'origin', branch]):
			Shell.success('Push success!')
			return True
		return False

	"""
	Tag Handling
	"""
	def tag_create(self, deploy_tag=''):
		if self.is_enabled():
			git_tag = self.create_git_version_tag(deploy_tag)

			if APISettings.PATCH_AUTO_BRANCH_COMMIT | APISettings.GIT_TAG_AUTO_COMMIT:
				if self.git_add():
					if self.git_commit(git_tag):
						if APISettings.PATCH_AUTO_BRANCH_PUSH:
							self.branch_push()
					return False
				return False

			if self.git_tag(git_tag):
				return True
		return False

	def tag_delete(self):
		if self.is_enabled():
			pass

	@classmethod
	def tag_push(cls):
		Shell.msg('Pushing tags...')
		call(['git', 'push', 'origin', '--tags'])

Git = Git()
