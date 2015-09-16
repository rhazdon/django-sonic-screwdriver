from optparse import make_option
from django.core.management.base import BaseCommand

from django_sonic_screwdriver.settings import api_settings
from django_sonic_screwdriver.version_handler import VersionHandler
from django_sonic_screwdriver.git import Git


class Command(BaseCommand):

	help = 'Command "patch" will help you to increase the version number of your project in a easy way.'

	option_list = BaseCommand.option_list + (
		make_option('--major', '-M', action='store_true', dest='major', default=False,
					help='Set major number'),
		make_option('--minor', '-m', action='store_true', dest='minor', default=False,
					help='Set minor number'),
		make_option('--patch', '-p', action='store_true', dest='patch', default=False,
					help='Ste patch number'),
		make_option('--dev', '-d', action='store_true', dest='dev', default=False,
					help='Set dev release (e.g. 1.2.1dev1)'),
		make_option('--alpha', '-a', action='store_true', dest='alpha', default=False,
					help='Set alpha release (e.g. 1.2.1a1)'),
		make_option('--beta', '-b', action='store_true', dest='beta', default=False,
					help='Set beta release (e.g. 1.2.1b1)'),
		make_option('--release-candidate', '-r', action='store_true', dest='rc', default=False,
					help='Set release candidate release (e.g. 1.2.1rc1).'),
		make_option('--force', '-f', action='store_true', dest='force', default=False,
					help='')
	)

	def handle(self, *args, **options):

		"""
		Check, how much options are true.
		If option '--force', '-f' is set this part will be skipped.
		"""
		if not options['force']:
			counter = 0
			for key in options:
				if options[key]:
					counter += 1

			# If no options are set, do a normal patch
			if counter == 1:
				options['patch'] = True

			# more then one options are not enabled per default
			if counter >= 3:
				exit('It is not recommended to use more then one parameter. Use -f to force your command.')
		###########################################################################################

		if options['major']:
			VersionHandler.set_major()

		if options['minor']:
			VersionHandler.set_minor()

		if options['patch']:
			VersionHandler.set_patch(VersionHandler.PATCH_NORMAL)

		if options['dev']:
			VersionHandler.set_patch(VersionHandler.PATCH_DEV)

		if options['alpha']:
			VersionHandler.set_patch(VersionHandler.PATCH_ALPHA)

		if options['beta']:
			VersionHandler.set_patch(VersionHandler.PATCH_BETA)

		if options['rc']:
			VersionHandler.set_patch(VersionHandler.PATCH_RC)

		if api_settings.GIT_AUTO_BRANCH:
			Git.branch_create()
			if api_settings.GIT_AUTO_COMMIT:
				Git.branch_commit()
				if api_settings.GIT_AUTO_COMMIT_PUSH:
					Git.branch_push()

		if api_settings.GIT_AUTO_TAG:
			Git.tag_create()
			if api_settings.GIT_AUTO_TAG_PUSH:
				Git.tag_push()
