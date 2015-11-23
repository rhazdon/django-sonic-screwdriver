from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git
from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.utils.shell import Shell


class Command(BaseCommand):

    args = 'tag'
    help = 'Remove last tag.'

    # option_list = BaseCommand.option_list + (
    #     make_option('tag', nargs='+', dest='tag', default=False, type=str,
    #                 help='Specify a tag, if you want. Otherwise the last tag will be removed.'),
    # )

    # def add_arguments(self, parser):
    #     parser.add_argument('tag', nargs='+', type=str, default='0',
    #                          help='Specify a tag, if you want. Otherwise the last tag will be removed.')

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
