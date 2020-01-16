import pytest
from mock import patch, Mock, MagicMock

from currencies.utils import (
    get_data,
    get_new_rates,
    get_rates,
    get_rates_coinmarketcap,
    get_rates_exchangeratesapi,
    update_rates,
)
from currencies.models import Currency


def test_get_data():
    with patch('currencies.utils.requests.get') as get_data_mock:
        response_mock = Mock()
        response_mock.content = '{"test": 123}'
        response_mock.raise_for_status = MagicMock()

        get_data_mock.return_value = response_mock

        assert isinstance(get_data(''), dict)


def test_get_rates_exchangeratesapi():
    data = get_rates_exchangeratesapi()
    symbols = {Currency.GBP, Currency.USD, Currency.RUB}
    assert symbols.issubset(set(data))


def test_get_rates_coinmarketcap():
    data = get_rates_coinmarketcap()
    symbols = {Currency.BTC}
    assert symbols.issubset(set(data))


@patch('currencies.utils.get_rates_exchangeratesapi')
@patch('currencies.utils.get_rates_coinmarketcap')
def test_get_new_rates(coinmarketcap_mock, exchangeratesapi_mock):
    coinmarketcap_mock.return_value = {Currency.BTC: 0}
    exchangeratesapi_mock.return_value = {Currency.GBP: 0, Currency.USD: 0, Currency.RUB: 0}

    symbols = set(Currency.CURRENCIES)
    symbols.remove(Currency.BASE)
    data = get_new_rates()
    assert symbols.issubset(set(data))


@pytest.mark.django_db
def test_get_rates():
    assert get_rates() == {'BTC': 0.00012714890572313473, 'GBP': 0.85618, 'RUB': 68.2418, 'USD': 1.1115}


@patch('currencies.utils.get_new_rates')
@pytest.mark.django_db
def test_update_rates(get_new_rates_mock):
    get_new_rates_mock.return_value = {'RUB': 0.1, 'USD': 1.1115}
    rub_count = Currency.objects.filter(currency=Currency.RUB).count()
    usd_count = Currency.objects.filter(currency=Currency.USD).count()
    update_rates()
    assert Currency.objects.filter(currency=Currency.RUB).order_by('-id').first().rate == 0.1
    assert Currency.objects.filter(currency=Currency.USD).order_by('-id').first().rate == 1.1115
    assert Currency.objects.filter(currency=Currency.RUB).count() == rub_count + 1
    assert Currency.objects.filter(currency=Currency.USD).count() == usd_count
