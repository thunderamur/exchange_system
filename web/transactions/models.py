from django.db import models, transaction

from balances.logic import update_balance
from currencies.models import Currency
from transactions.logic import get_amount


class TransactionManager(models.Manager):
    def create(self, **kwargs):
        from_user = kwargs.get('from_user')
        to_user = kwargs.get('to_user')
        currency = kwargs.get('currency')
        amount = kwargs.get('amount')

        from_amount = get_amount(amount, currency, from_user.currency)
        to_amount = get_amount(amount, currency, to_user.currency)

        with transaction.atomic():
            transaction_ = super().create(**kwargs)
            update_balance(from_user, -from_amount)
            update_balance(to_user, to_amount)

        return transaction_


class Transaction(models.Model):
    from_user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='from_user')
    to_user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='to_user')
    currency = models.CharField(choices=Currency.CURRENCY_CHOICES, max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    objects = TransactionManager()

    def __str__(self):
        return f'[{self.created}] {self.from_user} => {self.to_user}'

    class Meta:
        ordering = ('-id',)
