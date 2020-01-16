from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

User = get_user_model()


class TransactionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        transactions = Transaction.objects.filter(Q(from_user=user) | Q(to_user=user))
        serializer = TransactionSerializer(transactions, many=True)

        return Response({'data': serializer.data})

    @staticmethod
    def post(request):
        from_user = request.user
        to_user = User.objects.get(email=request.POST.get('user'))
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        data = {
            'from_user': from_user.pk,
            'to_user': to_user.pk,
            'amount': amount,
            'currency': currency,
        }
        transaction_serializer = TransactionSerializer(data=data, partial=True)

        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return Response({
                'status_code': status.HTTP_201_CREATED,
            })

        return Response({
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'errors': transaction_serializer.errors,
        })
