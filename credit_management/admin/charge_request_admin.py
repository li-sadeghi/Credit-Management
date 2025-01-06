from django.contrib import admin
from credit_management.models import ChargeRequest


@admin.register(ChargeRequest)
class ChargeRequestAdmin(admin.ModelAdmin):
    """Admin interface configuration for the ChargeRequest model.

    This class customizes the display and behavior of the ChargeRequest model in the Django admin interface.
    It provides a list view with specific fields and allows editing of the acceptance status directly.
    """

    model = ChargeRequest
    list_display = ("seller_full_name", "seller_phone_number", "is_accepted")
    list_editable = ("is_accepted",)

    def seller_full_name(self, obj: ChargeRequest):
        """Returns the full name of the seller associated with the charge request."""
        return obj.seller.full_name

    def seller_phone_number(self, obj: ChargeRequest):
        """Returns the phone number of the seller associated with the charge request."""
        return obj.seller.phone_number

    seller_full_name.short_description = "Seller Full Name"
    seller_phone_number.short_description = "Seller Phone Number"

    def get_queryset(self, request):
        """Returns a queryset of ChargeRequest instances that have not been accepted."""
        queryset = super().get_queryset(request)
        return queryset.filter(is_accepted=False)
