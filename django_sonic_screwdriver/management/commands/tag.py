from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git
from django_sonic_screwdriver.version_handler import VersionHandler


class Command(BaseCommand):

	help = 'Creates Authentification Tokens'

	option_list = BaseCommand.option_list + (
		make_option('--major', '-M', action='store_true', dest='major', default=False,
					help='Increase major number'),
		make_option('--minor', '-m', action='store_true', dest='minor', default=False,
					help='Increase minor number'),
		make_option('--patch', '-p', action='store_true', dest='patch', default=False,
					help='Increase patch number'),
		make_option('--staging', action='store_true', dest='staging', default=False,
					help=''),
		make_option('--activate', action='store_true', dest='activate', default=False,
					help=''),
		make_option('--push', action='store_true', dest='push', default=False,
					help='Push tags.'),
	)

	def handle(self, *args, **options):
		pass
		# if options['major']:
		# 	VersionHandler.increase_major()
		#
		# if options['minor']:
		# 	VersionHandler.increase_minor()
		#
		# if options['patch']:
		# 	VersionHandler.increase_patch()
		#
		# if options['staging']:
		# 	pass
		#
		# if options['activate']:
		# 	pass
		#
		# if options['push']:
		# 	Git.git_push()
