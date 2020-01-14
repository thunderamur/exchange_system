from .models import Balance


def update_balance(user, amount):
    """
    :param user:
    :param amount: Decimal. Money with user's currency
    :return: Balance
    """
    balance = Balance.objects.filter(user=user).order_by('-id').first()
    return Balance.objects.create(
        user=user,
        currency=user.currency,
        amount=balance.amount + amount,
        flow=amount
    )
