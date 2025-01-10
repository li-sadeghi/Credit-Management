from django.urls import path
from credit_management.views import (
    TransferView,
    SellerTransactionAPIView,
    ChargeRequestCreateView,
)

urlpatterns = [
    path("api/v1/transfer/", TransferView.as_view(), name="transfer"),
    path(
        "api/v1/transactions/",
        SellerTransactionAPIView.as_view(),
        name="seller-transactions",
    ),
    path(
        "api/v1/charge-requests/",
        ChargeRequestCreateView.as_view(),
        name="charge-request-create",
    ),
]
