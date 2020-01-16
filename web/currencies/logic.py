import decimal
from datetime import datetime, timedelta

from pytz import utc

from .exceptions import NotCurrencyOnDateError, WrongDateFormatError
from .models import Currency


def get_utc_date(date):
    """
    :param date: str. %Y-%m-%d
    :return: datetime. Aware datetime
    """
    return datetime.strptime(date, '%Y-%m-%d').astimezone(utc)


# TODO: cache
def get_rate(currency, date=None):
    """
    :param currency: Currency.CURRENCIES.
    :param date: str | datetime. str format: %Y-%m-%d
    :return: float. Currency.rate.
    """
    if currency == Currency.BASE:
        return 1.0

    if date:
        if isinstance(date, str):
            date = get_utc_date(date)
        elif not isinstance(date, datetime):
            raise WrongDateFormatError
        date += timedelta(days=1)

    q = Currency.objects.filter(currency=currency)
    if date:
        q = q.filter(created__lte=date)

    currency_on_date = q.order_by('id').last()

    if not currency_on_date:
        raise NotCurrencyOnDateError

    return currency_on_date.rate


# TODO: cache
def get_ratio(from_currency, to_currency, date=None):
    """
    :param from_currency: Currency.CURRENCIES
    :param to_currency: Currency.CURRENCIES
    :param date: str | datetime. str format: %Y-%m-%d
    :return: float
    """
    from_rate = get_rate(from_currency, date)
    to_rate = get_rate(to_currency, date)
    return to_rate/from_rate


def get_convert_amount(from_amount, from_currency, to_currency):
    """
    :param from_amount: Decimal value to convert.
    :param from_currency: Currency of from_amount
    :param to_currency: Currency of result
    :return: Decimal
    """
    if from_currency == to_currency:
        return from_amount

    ratio = get_ratio(from_currency, to_currency)
    result = float(from_amount) * ratio
    return get_decimal(result, '1.00')


def get_decimal(value, fmt):
    """
    :param value: float
    :param fmt: str. Decimal.quantize format
    :return: Decimal
    """
    result = decimal.Decimal(value)
    return result.quantize(decimal.Decimal(fmt), decimal.ROUND_HALF_EVEN)
