import os
from subprocess import call

from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.utils.shell import Shell


def git_available(func):
    """
    Check, if a git repository exists in the given folder.
    """
    def inner(*args):

        os.chdir(APISettings.GIT_DIR)

        if call(['git', 'rev-parse']) == 0:
            return func(*args)

        Shell.fail('There is no git repository!')
        return exit(1)
    return inner
