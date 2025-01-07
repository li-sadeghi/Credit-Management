from django.urls import path
from credit_management.views import TransferView

urlpatterns = [
    path("api/v1/transfer/", TransferView.as_view(), name="transfer"),
]
