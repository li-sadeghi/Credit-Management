from rest_framework import serializers
from credit_management.models import ChargeRequest


class ChargeRequestSerializer(serializers.ModelSerializer):
    """Serializer for handling ChargeRequest data."""

    class Meta:
        model = ChargeRequest
        fields = ["amount"]
        read_only_fields = ["is_accepted"]

    def validate(self, data):
        """Ensure the user doesn't have a pending charge request."""
        request = self.context.get("request")
        seller = request.user.seller

        # Ensure the seller has no active charge requests
        if ChargeRequest.objects.filter(seller=seller, is_accepted=False).exists():
            raise serializers.ValidationError(
                "You already have a pending charge request."
            )

        return data
