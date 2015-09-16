from optparse import make_option
from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import Git
from django_sonic_screwdriver.settings import api_settings


class Command(BaseCommand):

	help = 'Tag your project.'

	option_list = BaseCommand.option_list + (
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
		Git.tag_create()

		if options['staging']:
			Git.tag_create(api_settings.GIT_STAGING_TAG)

		if options['activate']:
			Git.tag_create(api_settings.GIT_ACTIVATE_TAG)

		if options['delete']:
			Git.tag_delete()

		if options['push'] | api_settings.GIT_AUTO_TAG_PUSH:
			Git.tag_push()
