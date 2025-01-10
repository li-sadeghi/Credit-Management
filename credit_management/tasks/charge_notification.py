from celery import shared_task
from credit_management.models import Notification, Seller
from django.db.models import Count

CHARGE_NOTIFICATION_TEXT = "Please charge your account."


@shared_task
def create_charge_notification(sellser_id: int = None):
    """Creates a charge notification for the specified seller."""
    if sellser_id is None:
        return
    seller = Seller.objects.get(id=sellser_id)
    Notification.objects.create(seller=seller, text=CHARGE_NOTIFICATION_TEXT)


@shared_task
def find_sellers_for_notification():
    """
    Finds sellers who have a credit balance of 0 and no existing notifications.
    Then, creates a charge notification for each of these sellers.
    """
    sellers_to_notification = Seller.objects.annotate(
        notification_count=Count("notifications")
    ).filter(credit=0, notification_count=0)
    for seller in sellers_to_notification:
        create_charge_notification.delay(seller.id)
