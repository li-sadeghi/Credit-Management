from django.db import models
from _helper.models import TimeModel
from django.db.models import Sum
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

    @property
    def remain_balance(self):
        from credit_management.models import Transaction

        """Calculates the remaining balance for the seller using transactions."""
        transactions = Transaction.objects.filter(seller=self)
        total_increase = (
            transactions.filter(transaction_type="d").aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        total_decrease = (
            transactions.filter(transaction_type="w").aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

        return total_increase - total_decrease

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
