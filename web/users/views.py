from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse
from rest_framework import generics, status

from balances.models import Balance
from users.serializers import UserSerializer

User = get_user_model()


class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        currency = request.POST['currency']
        start_balance = request.POST['start_balance']
        with transaction.atomic():
            user = User(
                email=email,
                currency=currency,
            )
            user.set_password(password)
            user.save()
            balance = Balance.objects.create(
                user=user,
                currency=currency,
                amount=start_balance,
                flow=start_balance,
            )
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if balance:
            status_code = status.HTTP_201_CREATED
        return JsonResponse(data={
            'status_code': status_code,
        })
