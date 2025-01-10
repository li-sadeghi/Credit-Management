from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from credit_management.models import Transaction
from credit_management.serializers import TransferSerializer
from _helper.permissions import IsSeller


class TransferView(APIView):
    """API endpoint for handling fund transfers between sellers.

    Methods:
        post(request, *args, **kwargs):
            Handles the POST request to process a fund transfer.
    """

    permission_classes = [IsSeller]

    def post(self, request, *args, **kwargs):
        """Handles a POST request to transfer funds between sellers.

        Args:
            request (Request): The HTTP request object containing transfer data in the body.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating the success or failure of the transfer.

        Request Data:
            - sender_phone (str): The phone number of the sender.
            - receiver_phone (str): The phone number of the receiver.
            - amount (int): The amount to transfer.

        Successful Response:
            - HTTP 200 OK: {"message": "Transfer successful."}

        Error Responses:
            - HTTP 400 Bad Request: If validation fails or an error occurs during the transfer.
                Example: {"error": "Error message"} or {"field": ["Validation error"]}

        Raises:
            serializers.ValidationError: If the request data is invalid.
            Exception: If an error occurs during the atomic transaction.
        """
        serializer = TransferSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            sender = serializer.validated_data["sender"]
            receiver = serializer.validated_data["receiver"]
            amount = serializer.validated_data["amount"]

            try:
                with transaction.atomic():
                    # Create a decrease transaction for the sender
                    Transaction.objects.create(
                        seller=sender,
                        transaction_type=Transaction.TransactionType.TYPE_DECREASE,
                        amount=amount,
                    )

                    # Create an increase transaction for the receiver
                    Transaction.objects.create(
                        seller=receiver,
                        transaction_type=Transaction.TransactionType.TYPE_INCREASE,
                        amount=amount,
                    )

                return Response(
                    {"message": "Transfer successful."}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
