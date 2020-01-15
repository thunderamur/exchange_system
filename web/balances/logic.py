from decimal import Decimal

from .exceptions import NotEnoughBalanceError
from .models import Balance


def get_balance(user):
    """
    :param user:
    :return: Balance. Actual user's balance.
    """
    return Balance.objects.filter(user=user).order_by('id').last()


def create_new_balance(user, amount):
    """
    :param user:
    :param amount: Decimal. Flow of money with user's currency
    :return: Balance
    """
    balance = get_balance(user)
    current_amount = 0
    if balance:
        current_amount = balance.amount

    new_amount = current_amount + amount

    if new_amount < Decimal('0.00'):
        raise NotEnoughBalanceError

    return Balance.objects.create(
        user=user,
        currency=user.currency,
        amount=new_amount,
    )
