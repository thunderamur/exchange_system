from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from balances.models import Balance
from users.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id)
        serializer = UserSerializer(user, many=True)

        return Response({'data': serializer.data})

    def post(self, request):
        user_serializer = UserCreateSerializer(data=request.data)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if user_serializer.is_valid():
            user_serializer.save()
            status_code = status.HTTP_201_CREATED

        return Response({
            'status_code': status_code,
        })
