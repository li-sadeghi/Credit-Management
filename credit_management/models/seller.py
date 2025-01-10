from django.db import models
from _helper.models import TimeModel
from _helper.validators import phone_number_validator
from django.contrib.auth.models import User


class Seller(TimeModel):
    """Represents a seller in the system.

    Attributes:
        user (OneToOneField): The user associated with the seller.
        full_name (CharField): The full name of the seller.
        phone_number (CharField): The phone number of the seller.
        credit (FloatField): The credit amount associated with the seller.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller",
        verbose_name="User",
        null=True,
        blank=True,
    )

    full_name = models.CharField(
        max_length=60,
        verbose_name="Full Name",
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name="Phone Number",
        validators=(phone_number_validator,),
        unique=True,
        db_index=True,
    )

    credit = models.FloatField(
        default=0.0,
        verbose_name="Credit",
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns the string representation of the seller."""
        return self.full_name + f" with phone {self.phone_number}"

    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
