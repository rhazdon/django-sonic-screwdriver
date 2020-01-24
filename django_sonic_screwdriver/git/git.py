from subprocess import call, check_output

from django_sonic_screwdriver.settings import api_settings
from django_sonic_screwdriver.version import version
from django_sonic_screwdriver.utils import shell
from django_sonic_screwdriver.git.decorators import git_available


GIT_OPTIONS = {
    "DEVELOPMENT": "development",
    "STAGING": "staging",
    "PRODUCTION": "production",
}


class Git:
    @staticmethod
    def create_git_version_tag(deploy_tag):
        if deploy_tag != "":
            deploy_tag += "-"
        return str(deploy_tag + "v" + version.get_version())

    @staticmethod
    @git_available
    def get_current_branch():
        current_branch = str(check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]))
        return current_branch[2:][: (current_branch.__len__() - 5)]

    @staticmethod
    @git_available
    def get_latest_tag():
        latest_tag_hash = str(
            check_output(["git", "rev-list", "--tags", "--max-count=1"])
        )
        latest_tag = str(
            check_output(
                [
                    "git",
                    "describe",
                    "--tags",
                    latest_tag_hash[2:][: (latest_tag_hash.__len__() - 5)],
                ]
            )
        )
        return latest_tag[2:][: (latest_tag.__len__() - 5)]

    @staticmethod
    @git_available
    def check_existence_of_staging_tag_in_remote_repo():
        """
        This method will check, if the given tag exists as a staging
        tag in the remote repository.

        The intention is, that every tag, which should be deployed
        on a production environment, has to be deployed on a staging environment before.
        """
        staging_tag = Git.create_git_version_tag(api_settings.GIT_STAGING_PRE_TAG)

        command_git = "git ls-remote -t"
        command_awk = "awk '{print $2}'"
        command_cut_1 = "cut -d '/' -f 3"
        command_cut_2 = "cut -d '^' -f 1"
        command_sort = "sort -b -t . -k 1,1nr -k 2,2nr -k 3,3r -k 4,4r -k 5,5r"
        command_uniq = "uniq"

        command = (
            command_git
            + " | "
            + command_awk
            + " | "
            + command_cut_1
            + " | "
            + command_cut_2
            + " | "
            + command_sort
            + " | "
            + command_uniq
        )

        list_of_tags = str(check_output(command, shell=True))

        if staging_tag in list_of_tags:
            return True
        return False

    @staticmethod
    def __debug(command, dry=False):
        """
        This method will be called, if the debug mode is on.
        """
        if dry:
            command.append("--dry-run")
        shell.debug(command)

        if dry:
            call(command)
        exit(1)

    # Git Basic Methods
    @staticmethod
    @git_available
    def __git_tag(git_tag):
        """
        Create new tag.
        The function call will return 0 if the command success.
        """
        command = ["git", "tag", "-a", git_tag, "-m", "'" + git_tag + "'"]
        shell.msg("Create tag from version " + git_tag)

        if api_settings.DEBUG:
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
        command = ["git", "tag", "-s", git_tag, "-m", "'" + git_tag + "'"]
        shell.msg("Create signed tag version " + git_tag + " with GPG")

        if api_settings.DEBUG:
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
        command = ["git", "push", "origin", "--tags"]
        shell.msg("Pushing tags...")

        if api_settings.DEBUG:
            Git.__debug(command, True)

        call(command)

    @staticmethod
    @git_available
    def __git_tag_delete(git_tag):
        """
        Delete last tag.
        The function call will return 0 if the command success.
        """
        command = ["git", "tag", "-d", "'" + git_tag + "'"]
        shell.msg("Delete tag.")

        if api_settings.DEBUG:
            Git.__debug(command, False)

        call(command)

    @git_available
    def __git_push(self):
        branch = self.get_current_branch
        command = ["git", "push", "-u", "origin", branch]
        shell.msg("Pushing branch " + branch + " to server...")

        if api_settings.DEBUG:
            Git.__debug(command, True)

        if not call(command):
            shell.success("Push success!")

    # Public Methods
    def tag(self, deploy_tag=""):
        """
        Function is public.
        Create a tag for current commit / branch.

        :param deploy_tag:
        :return:
        """
        if (
            api_settings.SECURE_TAGGING
            and deploy_tag == api_settings.GIT_ACTIVATE_PRE_TAG
        ):
            if self.check_existence_of_staging_tag_in_remote_repo():
                pass
            else:
                shell.fail(
                    "SECURE TAGGING is TRUE! That means, before you are able to "
                    "create a production tag, you need to deploy the software on "
                    "a staging environment."
                )
        self.__git_tag(self.create_git_version_tag(deploy_tag))

    def push_tags(self):
        """
        Function is public.
        Push tags.

        :return:
        """
        self.__git_tag_push()

    def tag_delete(self, tag):
        """
        Function is public.
        Push tags.

        :return:
        """
        if tag:
            self.__git_tag_delete(tag)
        self.__git_tag_delete(self.get_latest_tag())


git = Git()
