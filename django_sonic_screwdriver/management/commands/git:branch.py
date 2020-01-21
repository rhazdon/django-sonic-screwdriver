from django.core.management.base import BaseCommand

from django_sonic_screwdriver.git import git


class Command(BaseCommand):

    help = "Create new branch from current version."

    def add_arguments(self, parser):
        parser.add_argument(
            "--default",
            action="store_true",
            dest="default",
            default=False,
            help="(is default)",
        )

    def handle(self, *args, **options):
        git.add()
        # git.branch()
