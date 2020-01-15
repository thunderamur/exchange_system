from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command

from currencies.models import Currency
from currencies.utils import update_rates
from transactions.models import Transaction


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Load fixtures')

        fixtures = [
            'test_fixtures/User.json',
            'test_fixtures/Currency.json',
            'test_fixtures/Balance.json',
        ]

        try:
            call_command('loaddata', *fixtures)
        except Exception as exc:
            print(f'Problem in one of fixtures: {fixtures}: {exc}')

        print('Update rates of currencies')

        update_rates()

        ue = User.objects.get(pk=2)
        uu = User.objects.get(pk=3)
        ur = User.objects.get(pk=4)

        Transaction.objects.create(from_user=uu, to_user=ur, currency=Currency.USD, amount=Decimal('1.00'))
        Transaction.objects.create(from_user=ur, to_user=ue, currency=Currency.EUR, amount=Decimal('1.00'))
