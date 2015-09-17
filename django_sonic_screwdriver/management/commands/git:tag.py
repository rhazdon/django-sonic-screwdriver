from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git
from django_sonic_screwdriver.settings import APISettings


class Command(BaseCommand):

	help = 'Tag your project.'

	option_list = BaseCommand.option_list + (
		make_option('--default', action='store_true', dest='default', default=False,
					help='(is default)'),
		make_option('--staging', action='store_true', dest='staging', default=False,
					help='Create a staging tag (e.g. staging-v1.2.3)'),
		make_option('--activate', action='store_true', dest='activate', default=False,
					help='Create a activate tag (e.g. activate-v1.2.3)'),
		make_option('--delete-last', '-d', action='store_true', dest='delete', default=False,
					help='Delete last tag'),
		make_option('--push', action='store_true', dest='push', default=False,
					help='Push tags'),
	)

	def handle(self, *args, **options):
		"""
		:param args:
		:param options:
		:return:
		"""
		counter = 0
		for key in options:
			if options[key]:
				counter += 1

		# If no options are set, do a normal patch
		if counter == 1:
			options['default'] = True
		###########################################################################################
		tag_succeed = 1

		if APISettings.GIT_TAG_AUTO_COMMIT:
			Git.git_add()
			Git.branch_commit()

		if options['default']:
			tag_succeed = Git.tag_create()

		if options['staging']:
			tag_succeed = Git.tag_create(APISettings.GIT_STAGING_TAG)

		if options['activate']:
			tag_succeed = Git.tag_create(APISettings.GIT_ACTIVATE_TAG)

		if options['delete']:
			Git.tag_delete()

		if options['push'] | APISettings.GIT_AUTO_TAG_PUSH:
			if tag_succeed:
				Git.tag_push()
