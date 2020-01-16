from django.urls import path

from transactions import views

app_name = 'transactions'

urlpatterns = [
    path('', views.TransactionAPIView.as_view(), name='transaction'),
]
