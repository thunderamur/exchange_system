from django.db import models


class Currency(models.Model):
    EUR = 'EUR'
    USD = 'USD'
    GBP = 'GBP'
    RUB = 'RUB'
    BTC = 'BTC'

    CURRENCIES = [
        EUR,
        USD,
        GBP,
        RUB,
        BTC,
    ]

    CURRENCY_CHOICES = tuple((c, c) for c in CURRENCIES)

    BASE = EUR

    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    rate = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.currency}: {self.rate} ({self.created})'

    class Meta:
        ordering = ['-id']
