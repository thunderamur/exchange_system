import pytest
from datetime import datetime
from decimal import Decimal
from pytz import utc

from currencies.exceptions import NotCurrencyOnDateError
from currencies.logic import (
    get_convert_amount,
    get_decimal,
    get_rate,
    get_ratio,
    get_utc_date,
)
from currencies.models import Currency


def test_get_utc_date():
    date = '2020-01-15'
    assert get_utc_date(date) == datetime.strptime(date, '%Y-%m-%d').astimezone(utc)


@pytest.mark.django_db
def test_get_rate():
    assert get_rate(Currency.BASE) == 1.0
    assert get_rate(Currency.RUB) == 68.2418
    date = '2020-01-14'
    assert get_rate(Currency.BASE, date=date) == 1.0
    assert get_rate(Currency.RUB, date=date) == 68.041

    with pytest.raises(NotCurrencyOnDateError):
        get_rate(Currency.USD, date=date)


@pytest.mark.django_db
def test_get_ratio():
    assert get_ratio(Currency.BASE, Currency.BASE) == 1.0
    assert get_ratio(Currency.BASE, Currency.RUB) == 68.2418
    assert get_ratio(Currency.USD, Currency.RUB) == 61.396131354026096
    date = '2020-01-14'
    assert get_ratio(Currency.BASE, Currency.BASE, date=date) == 1.0
    assert get_ratio(Currency.BASE, Currency.RUB, date=date) == 68.041


@pytest.mark.django_db
def test_get_convert_amount():
    assert get_convert_amount(Decimal('10.00'), Currency.USD, Currency.RUB) == Decimal('613.96')


def test_get_decimal():
    assert get_decimal(66.6666, '1.00') == Decimal('66.67')
