import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model

from balances.models import Balance

User = get_user_model()


@pytest.mark.django_db
def test_get_balance():
    user_rub = User.objects.get(email__startswith='rub')
    assert user_rub.get_balance() == Decimal('0.00')
