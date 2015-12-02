from subprocess import call, check_output
from django.core.exceptions import ObjectDoesNotExist

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

    @staticmethod
    @git_available
    def check_existens_of_staging_tag_in_remote_repo():
        """
        This method will check, if the given tag exists as a staging tag in the remote repository.

        The intention is, that every tag, which should be deployed on a production envirnment,
        has to be deployed on a staging environment before.
        """
        staging_tag = Git.create_git_version_tag(APISettings.GIT_STAGING_PRE_TAG)

        command_git = 'git ls-remote -t'
        command_awk = 'awk \'{print $2}\''
        command_cut_1 = 'cut -d \'/\' -f 3'
        command_cut_2 = 'cut -d \'^\' -f 1'
        command_sort = 'sort -b -t . -k 1,1nr -k 2,2nr -k 3,3r -k 4,4r -k 5,5r'
        command_uniq = 'uniq'

        command = command_git + ' | ' + command_awk + ' | ' + command_cut_1 + ' | ' + \
                  command_cut_2 + ' | ' + command_sort + ' | ' + command_uniq

        list_of_tags = str(check_output(command, shell=True))

        if staging_tag in list_of_tags:
            return True
        return False


    @staticmethod
    def __debug(command, dry=False):
        """
        This method will be called, if the debug mode
        is on.
        """
        if dry:
            command.append('--dry-run')
        Shell.debug(command)

        if dry:
            call(command)
        exit(1)

    # Git Basic Methods
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
            Git.__debug(command, True)

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
        command = ['git', 'tag', '-a', git_tag, '-m', '\'' + git_tag + '\'']
        Shell.msg('Create tag from version ' + git_tag)

        if APISettings.DEBUG:
            Git.__debug(command, False)

        if not call(command):
            return True
        return False

    @staticmethod
    @git_available
    def __git_tag_gpg(git_tag):
        """
        Create new tag with GPG signature.
        The function call will return 0 if the command success.
        """
        command = ['git', 'tag', '-s', git_tag, '-m', '\'' + git_tag + '\'']
        Shell.msg('Create signed tag version ' + git_tag + ' with GPG')

        if APISettings.DEBUG:
            Git.__debug(command, False)

        if not call(command):
            return True
        return False

    @staticmethod
    @git_available
    def __git_tag_push():
        """
        Push all tags.
        The function call will return 0 if the command success.
        """
        command = ['git', 'push', 'origin', '--tags']
        Shell.msg('Pushing tags...')

        if APISettings.DEBUG:
            Git.__debug(command, True)

        if not call(command):
            return True
        return False

    @staticmethod
    @git_available
    def __git_tag_delete(git_tag):
        """
        Delete last tag.
        The function call will return 0 if the command success.
        """
        command = ['git', 'tag', '-d', '\'' + git_tag + '\'']
        Shell.msg('Delete tag.')

        if APISettings.DEBUG:
            Git.__debug(command, False)

        if not call(command):
            return True
        return False

    @staticmethod
    @git_available
    def __git_push():
        command = ['git', 'push', '-u', 'origin', branch]
        branch = self.get_current_branch
        Shell.msg('Pushing branch ' + branch + ' to server...')

        if APISettings.DEBUG:
            Git.__debug(command, True)

        if not call(command):
            Shell.success('Push success!')
            return True
        return False

    # Public Methods
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
        if APISettings.SECURE_TAGGING and deploy_tag == APISettings.GIT_ACTIVATE_PRE_TAG:
            if self.check_existens_of_staging_tag_in_remote_repo():
                pass
            else:
                Shell.fail('SECURE TAGGING is TRUE! That means, before you are able to create a production tag, ' \
                           'you need to deploy the software on a staging envirnment.')
                return False
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
