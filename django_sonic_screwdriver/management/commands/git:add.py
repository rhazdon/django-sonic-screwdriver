from django.core.management.base import BaseCommand

from django_sonic_screwdriver.git import git


class Command(BaseCommand):

    help = 'Add files to Git repository. Supports all standard "git add ... ".'

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            "-n",
            action="store_true",
            dest="dry-run",
            default=False,
            help="Dry run.",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Be verbose.",
        )
        parser.add_argument(
            "--interactive",
            "-i",
            action="store_true",
            dest="interactive",
            default=False,
            help="Interactive picking.",
        )
        parser.add_argument(
            "--patch",
            "-p",
            action="store_true",
            dest="patch",
            default=False,
            help="Select hunks interactively.",
        )
        parser.add_argument(
            "--edit",
            "-e",
            action="store_true",
            dest="edit",
            default=False,
            help="Edit current diff and apply.",
        )
        parser.add_argument(
            "--force",
            "-f",
            action="store_true",
            dest="force",
            default=False,
            help="Allow adding otherwise ignored files.",
        )
        parser.add_argument(
            "--update",
            "-u",
            action="store_true",
            dest="update",
            default=False,
            help="Update tracked files.",
        )
        parser.add_argument(
            "--intent-to-add",
            "-N",
            action="store_true",
            dest="intent-to-add",
            default=False,
            help="Record only the fact that the path will be added later.",
        )
        parser.add_argument(
            "--all",
            "-A",
            action="store_true",
            dest="all",
            default=False,
            help="Add changes from all tracked and untracked files.",
        )
        parser.add_argument(
            "--ignore-removal",
            action="store_true",
            dest="ignore-removal",
            default=False,
            help="Ignore paths removed in the working tree (same as --no-all).",
        )
        parser.add_argument(
            "--refresh",
            action="store_true",
            dest="--refresh",
            default=False,
            help="Do not add, only refresh the index.",
        )
        parser.add_argument(
            "--ignore-errors",
            action="store_true",
            dest="--ignore-errors",
            default=False,
            help="Just skip files which cannot be added because of errors.",
        )
        parser.add_argument(
            "--ignore-missing",
            action="store_true",
            dest="--ignore-missing",
            default=False,
            help="Check if - even missing - files are ignored in dry run.",
        )

    def handle(self, *args, **options):
        arguments = []

        for key in options:
            if options[key]:
                arguments.append("--" + key)

        # Remove --verbosity
        arguments.remove("--verbosity")

        # Add the files
        git.add(arguments)
