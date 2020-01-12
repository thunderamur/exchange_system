from django.db import models

from currencies.models import Currency


class Transactions(models.Model):
    from_user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='from_user')
    to_user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='to_user')
    from_currency = models.CharField(choices=Currency.CURRENCY_CHOICES, max_length=3)
    to_currency = models.CharField(choices=Currency.CURRENCY_CHOICES, max_length=3)
    from_amount = models.DecimalField(max_digits=10, decimal_places=2)
    to_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} => {self.to_user}'
