from subprocess import call
from optparse import make_option
from django.core.management.base import BaseCommand


class Command(BaseCommand):

	help = 'Tag your project.'

	option_list = BaseCommand.option_list + (
		make_option('--default', action='store_true', dest='default', default=False,
					help=''),
		make_option('--upload', '-u', action='store_true', dest='upload', default=False,
					help=''),
	)

	def handle(self, *args, **options):

		counter = 0
		for key in options:
			if options[key]:
				counter += 1

		# If no options are set, do a normal patch
		if counter == 1:
			options['default'] = True
		###########################################################################################

		if options['default']:
			call(['python', 'setup.py', 'sdist', 'bdist_wheel'])

		if options['upload']:
			call(['python', 'setup.py', 'sdist', 'bdist_wheel', 'upload'])
