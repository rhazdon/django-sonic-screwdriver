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

	"""
	Basic Functions
	"""
	@staticmethod
	def create_git_version_tag(deploy_tag):
		if deploy_tag != '':
				deploy_tag += '-'
		return str(deploy_tag + 'v' + Version.get_version())

	@property
	def get_current_branch(self):
		current_branch = str(check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']))
		return current_branch[2:][:(current_branch.__len__()-5)]

	"""
	Basic Git Commands
	"""
	@staticmethod
	def __git_add():
		"""
		Add files to staging.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Adding files...')
		if not call(['git', 'add', '-A']):
			return True
		return False

	@staticmethod
	def __git_commit(git_tag):
		"""
		Commit files to branch.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Commit changes.')
		if not call(['git', 'commit', '-m', '\'' + git_tag + '\'']):
			return True
		return False

	@staticmethod
	def __git_tag(git_tag):
		"""
		Create new tag.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Create tag from version ' + git_tag)
		if not call(['git', 'tag', '-a', git_tag, '-m', '\'' + git_tag + '\'']):
			return True
		return False

	@staticmethod
	def __git_tag_gpg(git_tag):
		"""
		Create new tag with GPG signature.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Create signed tag version ' + git_tag + ' with GPG')
		if not call(['git', 'tag', '-s', git_tag, '-m', '\'' + git_tag + '\'']):
			return True
		return False

	@staticmethod
	def __git_push():
		branch = self.get_current_branch
		Shell.msg('Pushing branch ' + branch + ' to server...')
		if not call(['git', 'push', '-u', 'origin', branch]):
			Shell.success('Push success!')
			return True
		return False

	@staticmethod
	def __git_push_tag():
		"""
		Push all tags.
		The function call will return 0 if the command success.
		"""
		Shell.msg('Pushing tags...')
		if not call(['git', 'push', 'origin', '--tags']):
			return True
		return False

	"""
	Public Functions
	"""
	def add(self):
		"""
		Function is public.
		:return:
		"""
		if self.__git_add():
			return True
		return False

	def commit(self):
		"""
		Function is public.
		Commit staged files into current branch.
		:return:
		"""
		if self.__git_commit(self.create_git_version_tag('')):
			return True
		return False

	def push_branches(self):
		"""
		Function is public.
		Push branches.
		:return:
		"""
		if self.__git_push():
			return True
		return False

	def tag(self, deploy_tag=''):
		"""
		Function is public.
		Create a tag for current commit / branch.
		:param deploy_tag:
		:return:
		"""
		if self.__git_tag(self.create_git_version_tag(deploy_tag)):
			return True
		return False

	def push_tags(self):
		"""
		Function is public.
		Push tags.
		:return:
		"""
		if self.__git_push_tag():
			return True
		return False

	def tag_delete(self):
		"""

		:return:
		"""
		pass

Git = Git()
