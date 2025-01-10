from django.db import models
from _helper.models import TimeModel
from credit_management.models import Seller


class Notification(TimeModel):
    """Represents a notification for a seller.

    Attributes:
        seller (ForeignKey): A reference to the `Seller` model. Represents the seller to whom the notification belongs.
        text (CharField): The title or content of the notification.

    Methods:
        __str__: Returns the string representation of the notification text.
    """

    seller = models.ForeignKey(
        to=Seller,
        verbose_name="Seller",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    text = models.CharField(
        max_length=100,
        verbose_name="Notification Title",
    )

    def __str__(self):
        """Returns the string representation of the Notification."""
        return self.text
