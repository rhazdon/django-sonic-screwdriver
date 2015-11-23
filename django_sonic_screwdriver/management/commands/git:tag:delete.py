from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git
from django_sonic_screwdriver.settings import APISettings


class Command(BaseCommand):

    help = 'Remove last tag.'

    def handle(self, *args, **options):
        Git.tag_delete()
