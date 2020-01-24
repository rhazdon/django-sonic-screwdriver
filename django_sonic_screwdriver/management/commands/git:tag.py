from django.core.management.base import BaseCommand
from django_sonic_screwdriver.git import git
from django_sonic_screwdriver.settings import api_settings


class Command(BaseCommand):

    help = "Tag your project."

    def add_arguments(self, parser):
        parser.add_argument(
            "--default",
            action="store_true",
            dest="default",
            default=False,
            help="(is default)",
        )

        parser.add_argument(
            "--staging",
            action="store_true",
            dest="staging",
            default=False,
            help="Create a staging tag (e.g. staging-v1.2.3)",
        )

        parser.add_argument(
            "--production",
            action="store_true",
            dest="production",
            default=False,
            help="Create a production tag (e.g. activate-v1.2.3)",
        )

        parser.add_argument(
            "--push", action="store_true", dest="push", default=False, help="Push tags"
        )

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:
        """
        counter = 0
        tag_succeed = 1

        for key in options:
            if options[key]:
                counter += 1

        # If no options are set, do a normal patch
        if counter == 1:
            options["default"] = True

        if options["default"]:
            tag_succeed = git.tag()

        if options["staging"]:
            tag_succeed = git.tag(api_settings.GIT_STAGING_PRE_TAG)

        if options["production"]:
            tag_succeed = git.tag(api_settings.GIT_ACTIVATE_PRE_TAG)

        if options["push"] | api_settings.GIT_TAG_AUTO_TAG_PUSH:
            if tag_succeed:
                git.push_tags()
