from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git


class Command(BaseCommand):

    help = 'Add files to Git repository. Supports all standard "git add ... ".'

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n', action='store_true', dest='dry-run', default=False,
                    help='Dry run.'),
        make_option('--verbose', action='store_true', dest='verbose', default=False,
                    help='Be verbose.'),
        make_option('--interactive', '-i', action='store_true', dest='interactive', default=False,
                    help='Interactive picking.'),
        make_option('--patch', '-p', action='store_true', dest='patch', default=False,
                    help='Select hunks interactively.'),
        make_option('--edit', '-e', action='store_true', dest='edit', default=False,
                    help='Edit current diff and apply.'),
        make_option('--force', '-f', action='store_true', dest='force', default=False,
                    help='Allow adding otherwise ignored files.'),
        make_option('--update', '-u', action='store_true', dest='update', default=False,
                    help='Update tracked files.'),
        make_option('--intent-to-add', '-N', action='store_true', dest='intent-to-add', default=False,
                    help='Record only the fact that the path will be added later.'),
        make_option('--all', '-A', action='store_true', dest='all', default=False,
                    help='Add changes from all tracked and untracked files.'),
        make_option('--ignore-removal', action='store_true', dest='ignore-removal', default=False,
                    help='Ignore paths removed in the working tree (same as --no-all).'),
        make_option('--refresh', action='store_true', dest='--refresh', default=False,
                    help='Do not add, only refresh the index.'),
        make_option('--ignore-errors', action='store_true', dest='--ignore-errors', default=False,
                    help='Just skip files which cannot be added because of errors.'),
        make_option('--ignore-missing', action='store_true', dest='--ignore-missing', default=False,
                    help='Check if - even missing - files are ignored in dry run.'),

    )

    def handle(self, *args, **options):
        arguments = []

        for key in options:
            if options[key]:
                arguments.append('--' + key)

        # Remove --verbosity
        arguments.remove('--verbosity')

        # Add the files
        Git.add(arguments)
