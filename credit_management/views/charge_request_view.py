from rest_framework import generics
from _helper.permissions import IsSeller
from credit_management.models import ChargeRequest
from credit_management.serializers import ChargeRequestSerializer


class ChargeRequestCreateView(generics.CreateAPIView):
    """API view to create a charge request for the authenticated seller."""

    queryset = ChargeRequest.objects.all()
    serializer_class = ChargeRequestSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        """Associates the charge request with the authenticated seller."""
        seller = self.request.user.seller
        serializer.save(seller=seller)
