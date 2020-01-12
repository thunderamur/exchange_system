from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'currency']


class UserCreateSerializer(serializers.ModelSerializer):
    start_balance = serializers.DecimalField(label=_('Start balance'), max_digits=10, decimal_places=2)

    class Meta:
        model = User
        fields = ['email', 'password', 'currency', 'start_balance']
