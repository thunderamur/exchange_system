import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model

from balances.logic import create_new_balance

User = get_user_model()


@pytest.mark.django_db
def test_get_balance():
    assert User.objects.get(pk=1).get_balance() == Decimal('0.00')
    assert User.objects.get(pk=2).get_balance() == Decimal('11.00')


@pytest.mark.django_db
def test_create_new_balance():
    ue = User.objects.get(pk=2)
    create_new_balance(ue, Decimal('4.50'))
    assert ue.get_balance() == Decimal('15.50')
    create_new_balance(ue, Decimal('-5.50'))
    assert ue.get_balance() == Decimal('10.00')
