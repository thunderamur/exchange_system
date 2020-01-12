from django.db import models

from currencies.models import Currency


class Balance(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    currency = models.CharField(choices=Currency.CURRENCY_CHOICES, max_length=3, default=Currency.BASE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    flow = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount} {self.currency} (USER_ID: {self.user_id})'
