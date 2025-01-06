from django.contrib import admin
from credit_management.models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Seller model."""

    model = Seller
    list_display = (
        "full_name",
        "phone_number",
        "remain_balance",
    )
