from subprocess import call
from django.core.management.base import BaseCommand


class Command(BaseCommand):

	help = 'Upload project to pypi via twine.'

	def handle(self, *args, **options):
		call(['twine', 'upload', 'dist/*'])
