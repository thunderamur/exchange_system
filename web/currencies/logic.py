import decimal
from django.db.models import Q

from .models import Currency


# TODO: cache
def get_rate(currency, date=None):
    if currency == Currency.BASE:
        return 1.0

    q = Currency.objects.filter(currency=currency)
    if date:
        q = q.filter(date__lte=date)

    return q.order_by('-id').first().rate


# TODO: cache
def get_ratio(from_currency, to_currency, date=None):
    # q = Currency.objects.filter(Q(currency=from_currency) | Q(currency=to_currency))
    # if date:
    #     q = q.filter(datetime_lte=date)
    #
    # from_rate = None
    # to_rate = None
    # for c in q.order_by('currency', '-id').distinct('currency').all()
    #     if c.currency == from_currency:
    #         from_rate = c.rate
    #     if c.currency == to_currency:
    #         to_rate = c.rate

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
    ratio = get_ratio(from_currency, to_currency)
    result = float(from_amount) * ratio
    return get_decimal(result, '1.00')


def get_decimal(value, format):
    result = decimal.Decimal(value)
    return result.quantize(decimal.Decimal(format), decimal.ROUND_HALF_EVEN)
