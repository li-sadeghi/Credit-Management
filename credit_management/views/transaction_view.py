from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from credit_management.models import Seller, Transaction
from credit_management.serializers import TransactionSerializer
from _helper.permissions import IsSeller


class SellerTransactionAPIView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        # Get the seller instance
        seller = self.request.user.seller

        # Fetch transactions for the seller
        transactions = Transaction.objects.filter(seller=seller)

        # Serialize the transactions
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
