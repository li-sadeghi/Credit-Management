from django.db import models
from django.db.models import F
from _helper.models import TimeModel
from credit_management.models import Seller
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Transaction(TimeModel):
    """Represents a financial transaction for a seller.

    This model tracks financial transactions for sellers, such as
    increases or decreases in their balance. Each transaction records
    the seller, type of transaction, and the transaction amount.

    Attributes:
        seller (ForeignKey): The seller associated with the transaction.
        transaction_type (CharField): The type of transaction
            (e.g., increase or decrease).
        amount (PositiveIntegerField): The amount involved in the transaction.
    """

    seller = models.ForeignKey(
        to=Seller,
        verbose_name=_("Seller"),
        on_delete=models.CASCADE,
    )

    class TransactionType(models.TextChoices):
        """Enumeration for transaction types."""

        TYPE_DECREASE = "w", _("Decrease")
        TYPE_INCREASE = "d", _("Increase")

    transaction_type = models.CharField(
        max_length=1,
        choices=TransactionType.choices,
        verbose_name=_("Transaction Type"),
    )
    amount = models.FloatField(
        verbose_name=_("Transaction Amount"),
        validators=[MinValueValidator(0.01)], 
    )

    def save(self, *args, **kwargs):
        if self.transaction_type == "d":
            Seller.objects.filter(pk=self.seller.pk).update(
                credit=F("credit") + self.amount
            )
        else:
            Seller.objects.filter(pk=self.seller.pk).update(
                credit=F("credit") - self.amount
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
