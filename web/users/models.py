from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from balances.models import Balance
from currencies.models import Currency


class UserManager(BaseUserManager):
    def create(self, email, password=None, currency=None, start_balance=0):
        return self.create_user(email=email, password=password, currency=currency, start_balance=start_balance)

    def create_user(self, email, password=None, currency=None, start_balance=0):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        user = User(
            username=email,
            email=email,
            currency=currency,
        )
        user.set_password(password)

        balance = Balance(
            user=user,
            currency=currency,
            amount=start_balance,
            flow=start_balance,
        )

        with transaction.atomic():
            user.save(using=self._db)
            balance.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Use for login.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    currency = models.CharField(choices=Currency.CURRENCY_CHOICES, max_length=3, default=Currency.BASE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def save(self, start_balance=0, *args, **kwargs,):
    #     email = kwargs.get('email')
    #     password = kwargs.get('password')
    #     currency = kwargs.get('currency')
    #
    #     user = User(
    #         email=email,
    #         currency=currency,
    #     )
    #     user.set_password(password)
    #
    #     balance = Balance(
    #         user=user,
    #         currency=currency,
    #         amount=start_balance,
    #         flow=start_balance,
    #     )
    #
    #     with transaction.atomic():
    #         super().save(*args, **kwargs)
    #         balance.save()

    def get_balance(self):
        balance = Balance.objects.filter(user=self.id).order_by('id').last()
        if balance:
            return Balance.objects.filter(user=self.id).order_by('id').last().amount
