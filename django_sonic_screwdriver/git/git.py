from subprocess import call, check_output

from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.version.version import Version
from django_sonic_screwdriver.utils import Shell
from django_sonic_screwdriver.git.decorators import git_available


GIT_OPTIONS = {
    'DEVELOPMENT': 'development',
    'STAGING': 'staging',
    'PRODUCTION': 'production',
}


class Git(object):

    @staticmethod
    def create_git_version_tag(deploy_tag):
        if deploy_tag != '':
            deploy_tag += '-'
        return str(deploy_tag + 'v' + Version.get_version())

    @staticmethod
    @git_available
    def get_current_branch():
        current_branch = str(check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']))
        return current_branch[2:][:(current_branch.__len__()-5)]

    @staticmethod
    @git_available
    def get_latest_tag():
        latest_tag_hash = str(check_output(['git', 'rev-list', '--tags', '--max-count=1']))
        latest_tag = str(check_output(['git', 'describe', '--tags', latest_tag_hash[2:][:(latest_tag_hash.__len__()-5)]]))
        return latest_tag[2:][:(latest_tag.__len__()-5)]

    """
    Basic Git Commands
    """
    @staticmethod
    @git_available
    def __git_add(args=''):
        """
        Add files to staging.
        The function call will return 0 if the command success.
        """
        command = ['git', 'add', '.']

        Shell.msg('Adding files...')
        if APISettings.DEBUG:
            Shell.debug('Execute "git add" in dry mode.')
            command.append('--dry-run')
            if not call(command):
                pass
            return True

        for key in args:
            command.append(key)
        if not call(command):
            pass
        return False

    # @staticmethod
    # @git_available
    # def __git_branch_create(git_tag):
    #     """
    #     Creates a new branch.
    #     The function call will return 0 if the command success.
    #     """
    #     Shell.msg('Create new branch with tag ' + git_tag)
    #     if APISettings.DEBUG:
    #         Shell.debug('Execute "git checkout -b" would create a new branch with name ' + git_tag + '.')
    #         return True
    #
    #     if not call(['git', 'checkout', '-b', '\'' + git_tag + '\'']):
    #         return True
    #     return False

    @staticmethod
    @git_available
    def __git_commit(git_tag):
        """
        Commit files to branch.
        The function call will return 0 if the command success.
        """
        Shell.msg('Commit changes.')
        if APISettings.DEBUG:
            Shell.debug('Execute "git commit" in dry mode.')
            if not call(['git', 'commit', '-m', '\'' + git_tag + '\'', '--dry-run']):
                pass
            return True

        if not call(['git', 'commit', '-m', '\'' + git_tag + '\'']):
            return True
        return False

    @staticmethod
    @git_available
    def __git_tag(git_tag):
        """
        Create new tag.
        The function call will return 0 if the command success.
        """
        Shell.msg('Create tag from version ' + git_tag)
        if APISettings.DEBUG:
            Shell.debug('Execute "git tag" would create a new tag with name ' + git_tag + '.')
            return True

        if not call(['git', 'tag', '-a', git_tag, '-m', '\'' + git_tag + '\'']):
            return True
        return False

    @staticmethod
    @git_available
    def __git_tag_gpg(git_tag):
        """
        Create new tag with GPG signature.
        The function call will return 0 if the command success.
            """
        Shell.msg('Create signed tag version ' + git_tag + ' with GPG')
        if APISettings.DEBUG:
            Shell.debug('Execute "git tag" would create a new tag with name ' + git_tag + ' signated witg gpg.')
            return True

        if not call(['git', 'tag', '-s', git_tag, '-m', '\'' + git_tag + '\'']):
            return True
        return False

    @staticmethod
    @git_available
    def __git_tag_push():
        """
        Push all tags.
        The function call will return 0 if the command success.
        """
        Shell.msg('Pushing tags...')
        if APISettings.DEBUG:
            Shell.debug('Execute "git push --tags" in debug mode.')
            if not call(['git', 'push', 'origin', '--tags', '--dry-run']):
                pass
            return True

        if not call(['git', 'push', 'origin', '--tags']):
            return True
        return False

    @staticmethod
    @git_available
    def __git_tag_delete(git_tag):
        """
        Delete last tag.
        The function call will return 0 if the command success.
        """
        Shell.msg('Delete tag.')
        if APISettings.DEBUG:
            Shell.debug('Execute "git tag -d" would delete tag with name ' + git_tag + '.')
            return True

        if not call(['git', 'tag', '-d', '\'' + git_tag + '\'']):
            return True
        return False

    @staticmethod
    @git_available
    def __git_push():
        branch = self.get_current_branch
        Shell.msg('Pushing branch ' + branch + ' to server...')
        if APISettings.DEBUG:
            Shell.debug('Execute "git push" in debug mode.')
            if not call(['git', 'push', '-u', 'origin', branch, '--dry-run']):
                Shell.success('Push success!')
                pass
            return True

        if not call(['git', 'push', '-u', 'origin', branch]):
            Shell.success('Push success!')
            return True
        return False

    """
    Public Functions
    """
    def add(self, args=''):
        """
        Function is public.
        :return:
        """
        if self.__git_add(args):
            return True
        return False

    # def branch_create(self):
    #     """
    #     Function is public.
    #     :return:
    #     """
    #     if self.__git_commit(Version.get_version()):
    #         return True
    #     return False

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
        if self.__git_tag_push():
            return True
        return False

    def tag_delete(self, tag):
        """
        Function is public.
        Push tags.
        :return:
        """
        if tag:
            if self.__git_tag_delete(tag):
                return True
            return False

        if self.__git_tag_delete(self.get_latest_tag()):
            return True
        return False

Git = Git()
