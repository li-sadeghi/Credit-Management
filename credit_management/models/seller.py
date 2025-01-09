from django.db import models
from _helper.models import TimeModel
from _helper.validators import phone_number_validator


class Seller(TimeModel):
    """Represents a seller in the system.

    Attributes:
        full_name (CharField): The full name of the seller.
        phone_number (CharField): The phone number of the seller.
    """

    full_name = models.CharField(
        max_length=60,
        verbose_name="Full Name",
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name="Phone Number",
        validators=(phone_number_validator,),
        unique=True,
    )

    credit = models.FloatField(default=0.0, verbose_name="Credit",)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
