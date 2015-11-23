import os
import shutil
from subprocess import call
from optparse import make_option
from django.core.management.base import BaseCommand

from django_sonic_screwdriver.utils.shell import Shell


class Command(BaseCommand):

    help = 'Export your project.'

    option_list = BaseCommand.option_list + (
        make_option('--wheel', '-w', action='store_true', dest='wheel', default=False,
                    help='Export project with wheel (recommended). Needs package wheel.'),
        make_option('--upload', '-u', action='store_true', dest='upload', default=False,
                    help='Upload Project.'),
    )

    def handle(self, *args, **options):
        clean_dist_dir()

        export = ['python', 'setup.py', 'sdist']

        if options['wheel']:
            export.append('bdist_wheel')
            call(export)
        else:
            call(export)

        if options['upload']:
            export.append('upload')
            call(export)


def clean_dist_dir():
    Shell.warn('Do you want to cleanup dist directory before? (Y/n)')
    confirmation = input()
    if confirmation != 'n':
        shutil.rmtree(os.path.join('dist'))
