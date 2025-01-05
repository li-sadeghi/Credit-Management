from django.db import models
from _helper.models import TimeModel
from credit_management.models import Seller
from django.utils.translation import gettext_lazy as _


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
    amount = models.PositiveIntegerField(
        verbose_name=_("Transaction Amount"),
    )

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
