from django.core.management.base import BaseCommand

from django_sonic_screwdriver.git import git


class Command(BaseCommand):

    help = "Push your tagged project."

    def handle(self, *args, **options):
        git.push_tags()
