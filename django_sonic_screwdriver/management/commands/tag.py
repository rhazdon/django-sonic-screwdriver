from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git.tag import increase_major, increase_minor, increase_revision


class Command(BaseCommand):

	help = 'Creates Authentification Tokens'

	option_list = BaseCommand.option_list + (
		make_option('--major', action='store_true', dest='major', default=False,
					help='Increase major number'),
		make_option('--minor', action='store_true', dest='minor', default=False,
					help='Increase minor number'),
		make_option('--revision', action='store_true', dest='revision', default=False,
					help='Increase revision number'),
	)

	def handle(self, *args, **options):
		if options['major']:
			increase_major()

		if options['minor']:
			increase_minor()

		if options['revision']:
			increase_revision()
