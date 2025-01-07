from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from credit_management.models import Seller, Transaction
from credit_management.serializers import TransactionSerializer

class SellerTransactionAPIView(APIView):
    def get(self, request, seller_id):
        # Get the seller instance
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            raise NotFound("Seller not found")

        # Fetch transactions for the seller
        transactions = Transaction.objects.filter(seller=seller)

        # Serialize the transactions
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
