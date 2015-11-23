from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git


class Command(BaseCommand):

    help = 'Create new branch from current version.'

    option_list = BaseCommand.option_list + (
        make_option('--default', action='store_true', dest='default', default=False,
                    help='(is default)'),
    )

    def handle(self, *args, **options):
        Git.add()
        # Git.branch()
