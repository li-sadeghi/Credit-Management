from rest_framework import serializers
from credit_management.models import Transaction, Seller


class SellerSerializer(serializers.ModelSerializer):
    credit = serializers.ReadOnlyField()

    class Meta:
        model = Seller
        fields = ("id", "full_name", "phone_number", "credit")


class TransactionSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["seller"] = SellerSerializer(instance.seller).data
        return representation
