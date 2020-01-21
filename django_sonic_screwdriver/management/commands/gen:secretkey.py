from django.core.management.base import BaseCommand
from random import choice


class Command(BaseCommand):
    help = "Generates a new SECRET_KEY."

    requires_system_checks = False

    def handle(self, *args, **options):
        return "".join(
            [
                choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
                for i in range(50)
            ]
        )
