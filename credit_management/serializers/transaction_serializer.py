from rest_framework import serializers
from credit_management.models import Transaction, Seller

class SellerSerializer(serializers.ModelSerializer):
    remain_balance = serializers.ReadOnlyField()

    class Meta:
        model = Seller
        fields = ("id", "full_name", "phone_number", "remain_balance")


class TransactionSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["seller"] = SellerSerializer(instance.seller).data
        return representation
