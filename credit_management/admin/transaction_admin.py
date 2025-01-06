from django.contrib import admin
from credit_management.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Seller model."""

    model = Transaction
    list_display = (
        "seller_full_name",
        "seller_phone_number",
        "amount",
        "transaction_type",
    )

    def seller_full_name(self, obj: Transaction):
        """Returns the full name of the seller associated with the transaction."""
        return obj.seller.full_name

    def seller_phone_number(self, obj: Transaction):
        """Returns the phone number of the seller associated with the transaction."""
        return obj.seller.phone_number

    def transaction_type(self, obj: Transaction):
        if obj.transaction_type == "w":
            return "Decrease"
        else:
            return "Increase"

    seller_full_name.short_description = "Seller Full Name"
    seller_phone_number.short_description = "Seller Phone Number"
    transaction_type.short_description = "Transaction Type"
