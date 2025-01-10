from django.core.exceptions import ValidationError
from django.db import models
from _helper.models import TimeModel
from credit_management.models import Seller
from django.core.validators import MinValueValidator


class ChargeRequest(TimeModel):
    """Represents a request to charge a seller's account.

    This model tracks requests made by sellers to add credit to their accounts.
    Each seller can have only one active charge request at a time.

    Attributes:
        seller (ForeignKey): The seller associated with the charge request.
        amount (FloatField): The requested amount to be charged in the account.
        is_accepted (BooleanField): Indicates whether the charge request has been accepted.
    """

    seller = models.ForeignKey(
        to=Seller,
        verbose_name="Seller",
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        verbose_name="Charge Amount",
        validators=[MinValueValidator(0.01)],
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name="Is Accepted",
    )

    def save(self, *args, **kwargs):
        if self.pk:
            old_object = ChargeRequest.objects.get(pk=self.pk)
            if old_object.is_accepted:
                raise ValidationError(
                    "This charge request has already been accepted and cannot be modified."
                )
            else:
                seller = Seller.objects.select_for_update().get(
                    phone_number=self.seller.phone_number
                )
                seller.credit += self.amount
                seller.save()
        elif self.is_accepted:
            raise ValidationError(
                "This charge request must be accepted in admin panel."
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
