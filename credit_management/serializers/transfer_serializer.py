from rest_framework import serializers
from credit_management.models import Seller


class TransferSerializer(serializers.Serializer):
    """Serializer for handling fund transfers between sellers.

    Attributes:
        sender_phone (CharField): The phone number of the sender (required, max length 13).
        receiver_phone (CharField): The phone number of the receiver (required, max length 13).
        amount (IntegerField): The amount to transfer (required, minimum value 1).

    Methods:
        validate(data):
            Validates the transfer request.
            Ensures sender and receiver are different, both exist, and the sender has sufficient balance.
    """

    receiver_phone = serializers.CharField(max_length=13, required=True)
    amount = serializers.IntegerField(min_value=1, required=True)

    def __init__(self, *args, **kwargs):
        # Pass the request object to the serializer
        self.request = kwargs.get("context", {}).get("request", None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        """Validates the transfer details.

        Args:
            data (dict): A dictionary containing the transfer details including:
                - sender_phone (str): Sender's phone number.
                - receiver_phone (str): Receiver's phone number.
                - amount (int): Amount to transfer.

        Returns:
            dict: The validated data with additional `sender` and `receiver` fields.

        Raises:
            serializers.ValidationError: If:
                - Sender and receiver phone numbers are the same.
                - Sender does not exist.
                - Sender's balance is insufficient.
                - Receiver does not exist.
        """
        sender = self.request.user.seller
        sender_phone = sender.phone_number
        receiver_phone = data.get("receiver_phone")
        amount = data.get("amount")

        if sender_phone == receiver_phone:
            raise serializers.ValidationError("Sender and receiver must be different.")

        if sender.credit < amount:
            raise serializers.ValidationError("Sender has insufficient balance.")

        try:
            receiver = Seller.objects.get(phone_number=receiver_phone)
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Receiver not found.")

        data["sender"] = sender
        data["receiver"] = receiver
        return data
