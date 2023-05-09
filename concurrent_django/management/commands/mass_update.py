from django.core.management import BaseCommand

from concurrent_django.exercises.mass_update import start


class Command(BaseCommand):
    help = "Start the mass update exercise"

    def handle(self, *args, **options):
        start()
