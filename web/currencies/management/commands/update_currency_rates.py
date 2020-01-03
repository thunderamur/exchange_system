from django.core.management.base import BaseCommand

from currencies.utils import update_rates


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_rates()
