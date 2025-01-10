from django.contrib import admin
from credit_management.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Notification model."""

    model = Notification
    list_display = (
        "seller",
        "text",
    )
