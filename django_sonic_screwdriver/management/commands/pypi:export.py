import os
import shutil

from django.core.management.base import BaseCommand
from subprocess import call

from django_sonic_screwdriver.utils.shell import shell


class Command(BaseCommand):

    help = "Export your project."

    def add_arguments(self, parser):

        parser.add_argument(
            "--no-wheel",
            action="store_true",
            dest="nowheel",
            default=False,
            help="Do not export project with wheel.",
        )

        parser.add_argument(
            "--upload",
            "-u",
            action="store_true",
            dest="upload",
            default=False,
            help="Upload Project.",
        )

    def handle(self, *args, **options):
        clean_dist_dir()

        export = ["python", "setup.py", "sdist"]

        if options["nowheel"]:
            call(export)
        else:
            export.append("bdist_wheel")
            call(export)

        if options["upload"]:
            export.append("upload")
            call(export)


def clean_dist_dir():
    shell.warn("Do you want to cleanup dist directory before? (Y/n)")
    confirmation = input()
    if confirmation != "n":
        shutil.rmtree(os.path.join("dist"))
