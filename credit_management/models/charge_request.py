from django.db import models
from _helper.models import TimeModel
from credit_management.models import Seller


class ChargeRequest(TimeModel):
    """Represents a request to charge a seller's account.

    This model tracks requests made by sellers to add credit to their accounts.
    Each seller can have only one active charge request at a time.

    Attributes:
        seller (ForeignKey): The seller associated with the charge request.
        amount (PositiveIntegerField): The requested amount to be charged in the account.
        is_accepted (BooleanField): Indicates whether the charge request has been accepted.
    """

    seller = models.ForeignKey(
        to=Seller,
        verbose_name="Seller",
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Charge Amount",
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name="Is Accepted",
    )

    def save(self, *args, **kwargs):
        from credit_management.models import Transaction

        if self.is_accepted:
            Transaction.objects.create(
                seller=self.seller,
                transaction_type="d",
                amount=self.amount,
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Charge Request"
        verbose_name_plural = "Charge Requests"

        constraints = [
            models.UniqueConstraint(
                fields=["seller"], name="unique_charge_request_per_seller"
            )
        ]
