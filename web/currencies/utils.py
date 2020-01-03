import json
import requests

from .models import Currency


def get_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.content)


def get_rates_exchangeratesapi(date=None, base=None, symbols=None):
    url = 'https://api.exchangeratesapi.io'

    if date is None:
        date = 'latest'
    if base is None:
        base = Currency.BASE

    url += f'/{date}?base={base}'

    if symbols:
        url += f'&symbols={symbols}'

    return get_data(url)


def get_rates_coinmarketcap(base=None, symbols=None):
    url = 'https://api.coinmarketcap.com/v1/ticker'

    if base is None:
        base = Currency.BASE

    price_key = f'price_{base.lower()}'
    url += f'/?convert={base}'
    symbol_list = None
    if symbols:
        symbol_list = [symbol.strip() for symbol in symbols.split(',')]

    rates = {}
    for data in get_data(url):
        symbol = data['symbol']
        if symbol_list and symbol not in symbol_list:
            continue
        rate = 1 / float(data[price_key])
        rates.update({symbol: rate})

    return {
        'rates': rates,
        'base': base,
    }


def get_new_rates(base=None):
    rates = get_rates_coinmarketcap(base=base)['rates']
    rates.update(get_rates_exchangeratesapi(base=base)['rates'])

    return rates


def get_rates():
    rates = {}
    for currency in Currency.objects.filter(currency__in=Currency.CURRENCIES).order_by('currency', '-datetime').\
            distinct('currency'):
        rates.update({currency.currency: currency.rate})
    return rates


def update_rates():
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
