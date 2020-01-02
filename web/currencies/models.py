from django.db import models


class Currency(models.Model):
    EUR = 'EUR'
    USD = 'USD'
    GBP = 'GBP'
    RUB = 'RUB'
    BTC = 'BTC'

    CURRENCY_CHOICES = (
        (EUR, EUR),
        (USD, USD),
        (GBP, GBP),
        (RUB, RUB),
        (BTC, BTC),
    )

    BASE = EUR

    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']
