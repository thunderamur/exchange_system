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
    return Balance.objects.create(
        user=user,
        currency=user.currency,
        amount=current_amount + amount,
    )
