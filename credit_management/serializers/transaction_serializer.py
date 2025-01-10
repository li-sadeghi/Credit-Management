from rest_framework import serializers
from credit_management.models import Transaction, Seller


class SellerSerializer(serializers.ModelSerializer):
    """Serializer for Seller model."""

    credit = serializers.ReadOnlyField()

    class Meta:
        model = Seller
        fields = ("id", "full_name", "phone_number", "credit")


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model.

    This serializer defines how to represent a transaction, including the related seller.
    It includes all fields from the Transaction model and uses the SellerSerializer to represent
    the associated seller information.
    """

    seller = SellerSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        """Custom representation for the Transaction model.

        This method overrides the default representation to ensure that the seller field is properly
        serialized using the SellerSerializer.

        Args:
            instance (Transaction): The transaction instance being serialized.

        Returns:
            dict: The serialized representation of the transaction, including the serialized seller.
        """
        representation = super().to_representation(instance)
        representation["seller"] = SellerSerializer(instance.seller).data
        return representation
