import json
import requests

from .models import Currency


def get_data(url):
    """
    :param url: str
    :return: dict
    """
    response = requests.get(url)
    response.raise_for_status()

    return json.loads(response.content)


def get_rates_exchangeratesapi(date=None, base=None, symbols=None):
    """
    :param date: str | datetime. str format: %Y-%m-%d
    :param base: Currency.CURRENCIES
    :param symbols: Currency.CURRENCIES
    :return: dict
    """
    url = 'https://api.exchangeratesapi.io'

    if date is None:
        date = 'latest'
    if base is None:
        base = Currency.BASE

    url += f'/{date}?base={base}'

    if symbols:
        url += f'&symbols={symbols}'

    data = get_data(url)

    return data['rates']


def get_rates_coinmarketcap(base=None):
    """
    :param base: Currency.CURRENCIES
    :return: dict
    """
    url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin'

    if base is None:
        base = Currency.BASE

    price_key = f'price_{base.lower()}'
    url += f'/?convert={base}'

    rates = {}
    for data in get_data(url):
        symbol = data['symbol']
        rate = 1 / float(data[price_key])
        rates.update({symbol: rate})

    return rates


def get_new_rates(base=None):
    """
    :param base: Currency.CURRENCIES
    :return: dict
    """
    rates = get_rates_coinmarketcap(base=base)
    symbols = f'{Currency.RUB},{Currency.USD},{Currency.GBP}'
    rates.update(get_rates_exchangeratesapi(base=base, symbols=symbols))

    return rates


def get_rates():
    """
    :return: dict
    """
    rates = {}
    for currency in Currency.objects.filter(currency__in=Currency.CURRENCIES).order_by('currency', '-id').\
            distinct('currency'):
        rates.update({currency.currency: currency.rate})

    return rates


def update_rates():
    """
    Update currency's rates. Used in manage.py command.
    """
    saved_rates = get_rates()
    new_rates = get_new_rates()
    for currency in Currency.CURRENCIES:
        if currency in new_rates and (
                currency not in saved_rates or
                new_rates[currency] != saved_rates[currency]
        ):
            Currency.objects.create(
                currency=currency,
                rate=new_rates[currency],
            )
