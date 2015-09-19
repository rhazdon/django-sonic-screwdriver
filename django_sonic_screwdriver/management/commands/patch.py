from optparse import make_option
from django.core.management.base import BaseCommand

from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.version import Version
from django_sonic_screwdriver.git import Git


class Command(BaseCommand):

	help = 'Command "patch" will help you to increase the version number of your project in a easy way.'

	option_list = BaseCommand.option_list + (
		make_option('--major', '-M', action='store_true', dest='major', default=False,
					help='Set major number'),
		make_option('--minor', '-m', action='store_true', dest='minor', default=False,
					help='Set minor number'),
		make_option('--patch', '-p', action='store_true', dest='patch', default=False,
					help='Set patch number'),
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
				# TODO: Raise Error!
				exit('It is not recommended to use more then one parameter. Use -f to force your command.')
		###########################################################################################

		if options['major']:
			Version.set_major()

		if options['minor']:
			Version.set_minor()

		if options['patch']:
			Version.set_patch()

		if options['dev']:
			Version.set_patch(Version.DEV)

		if options['alpha']:
			Version.set_patch(Version.ALPHA)

		if options['beta']:
			Version.set_patch(Version.BETA)

		if options['rc']:
			Version.set_patch(Version.RC)

		"""
		Automatics.
		Depends on User Settings.
		"""
		if APISettings.PATCH_AUTO_COMMIT:
			Git.add()
			Git.commit()

		if APISettings.PATCH_AUTO_TAG:
			Git.tag()
			if APISettings.PATCH_AUTO_TAG_PUSH:
				Git.push_tags()
