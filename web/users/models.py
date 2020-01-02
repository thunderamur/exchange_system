from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from currencies.models import Currency


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    currency = models.CharField(choices=Currency.CURRENCY_CHOICES, max_length=3, default=Currency.BASE)
