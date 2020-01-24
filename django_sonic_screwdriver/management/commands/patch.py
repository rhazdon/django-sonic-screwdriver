from django.core.management.base import BaseCommand
from django_sonic_screwdriver.settings import api_settings
from django_sonic_screwdriver.version import version
from django_sonic_screwdriver.git import git


class Command(BaseCommand):

    help = (
        'Command "patch" will help you to increase the version number of '
        "your project in a easy way."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--major",
            "-M",
            action="store_true",
            dest="major",
            default=False,
            help="Set major number",
        )

        parser.add_argument(
            "--minor",
            "-m",
            action="store_true",
            dest="minor",
            default=False,
            help="Set minor number",
        )

        parser.add_argument(
            "--patch",
            "-p",
            action="store_true",
            dest="patch",
            default=False,
            help="Set patch number",
        )

        parser.add_argument(
            "--dev",
            "-d",
            action="store_true",
            dest="dev",
            default=False,
            help="Set dev release (e.g. 1.2.1dev1)",
        )

        parser.add_argument(
            "--alpha",
            "-a",
            action="store_true",
            dest="alpha",
            default=False,
            help="Set alpha release (e.g. 1.2.1a1)",
        )

        parser.add_argument(
            "--beta",
            "-b",
            action="store_true",
            dest="beta",
            default=False,
            help="Set beta release (e.g. 1.2.1b1)",
        )

        parser.add_argument(
            "--release-candidate",
            "-r",
            action="store_true",
            dest="rc",
            default=False,
            help="Set release candidate release (e.g. 1.2.1rc1).",
        )

        parser.add_argument(
            "--force", "-f", action="store_true", dest="force", default=False, help=""
        )

    def handle(self, *args, **options):
        """
        Check, how much options are true.
        If option '--force', '-f' is set this part will be skipped.
        """
        if not options["force"]:
            counter = 0
            for key in options:
                if options[key]:
                    counter += 1

            # If no options are set, do a normal patch
            if counter == 1:
                options["patch"] = True

            # more then one options are not enabled per default
            if counter >= 3:
                # TODO: Raise Error!
                exit(
                    "It is not recommended to use more then one parameter. "
                    "Use -f to force your command."
                )

        if options["major"]:
            version.set_major()

        if options["minor"]:
            version.set_minor()

        if options["patch"]:
            version.set_patch()

        if options["dev"]:
            version.set_patch(version.DEV)

        if options["alpha"]:
            version.set_patch(version.ALPHA)

        if options["beta"]:
            version.set_patch(version.BETA)

        if options["rc"]:
            version.set_patch(version.RC)

        if api_settings.PATCH_AUTO_TAG:
            git.tag()
