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
        make_option('--production', action='store_true', dest='production', default=False,
                    help='Create a production tag (e.g. activate-v1.2.3)'),
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
            Git.add()
            Git.commit()

        if options['default']:
            tag_succeed = Git.tag()

        if options['staging']:
            tag_succeed = Git.tag(APISettings.GIT_STAGING_PRE_TAG)

        if options['production']:
            tag_succeed = Git.tag(APISettings.GIT_ACTIVATE_PRE_TAG)

        if options['push'] | APISettings.GIT_TAG_AUTO_TAG_PUSH:
            if tag_succeed:
                Git.push_tags()
