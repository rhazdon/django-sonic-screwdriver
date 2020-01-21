from django.core.management.base import BaseCommand

from django_sonic_screwdriver.git import git
from django_sonic_screwdriver.utils.shell import shell


class Command(BaseCommand):

    args = "tag"
    help = "Remove last or given tag."

    def handle(self, *args, **options):
        if args:
            shell.warn("Do you want to remove tag " + str(args[0]) + "? (Y/n)")
            confirmation = input()
            if confirmation != "n":
                git.tag_delete(str(args[0]))

        else:
            shell.warn("Do you want to remove tag " + git.get_latest_tag() + "? (Y/n)")
            confirmation = input()
            if confirmation != "n":
                git.tag_delete(None)
