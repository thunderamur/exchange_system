from currencies.logic import get_convert_amount


def get_amount(amount, from_currency, to_currency):
    from_amount = amount
    if from_currency != to_currency:
        from_amount = get_convert_amount(amount, from_currency, to_currency)

    return from_amount
