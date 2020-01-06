from django.contrib.auth import get_user_model
from rest_framework import generics
from users.serializers import UserSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
