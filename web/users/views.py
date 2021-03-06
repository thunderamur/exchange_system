from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        user_id = request.GET.get('user_id')
        q = User.objects
        if user_id:
            q = q.filter(id=user_id)
        serializer = UserSerializer(q, many=True)

        return Response({'data': serializer.data})

    @staticmethod
    def post(request):
        user_serializer = UserCreateSerializer(data=request.data)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if user_serializer.is_valid():
            user_serializer.save()
            status_code = status.HTTP_201_CREATED

        return Response({
            'status_code': status_code,
        })
