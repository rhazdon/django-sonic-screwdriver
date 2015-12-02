from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git
from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.utils.shell import Shell


class Command(BaseCommand):

    args = 'tag'
    help = 'Remove last or given tag.'


    def handle(self, *args, **options):
        if args:
            Shell.warn('Do you want to remove tag ' + str(args[0]) + '? (Y/n)')
            confirmation = input()
            if confirmation != 'n':
                Git.tag_delete(str(args[0]))

        else:
            Shell.warn('Do you want to remove tag ' + Git.get_latest_tag() + '? (Y/n)')
            confirmation = input()
            if confirmation != 'n':
                Git.tag_delete(None)
