from django.urls import path
from credit_management.views import TransferView, SellerTransactionAPIView

urlpatterns = [
    path("api/v1/transfer/", TransferView.as_view(), name="transfer"),
    path("api/v1/transactions/<int:seller_id>/", SellerTransactionAPIView.as_view(), name="seller-transactions"),
]
