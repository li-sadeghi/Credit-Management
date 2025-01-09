from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from credit_management.models import Seller, Transaction
from django.urls import reverse
from _helper.tests.factory import (
    create_dummy_seller,
    create_dummy_charge_request,
    create_dummy_transaction,
)


class TestTransactionView(APITestCase):
    """Test suite for the Transaction view."""

    def setUp(self):
        """Set up test environment by creating a dummy seller, charge request, and transactions."""
        self.seller = create_dummy_seller()
        charge = create_dummy_charge_request(seller=self.seller, amount=1000)
        charge.is_accepted = True
        charge.save()

        self.transaction1 = create_dummy_transaction(
            seller=self.seller, amount=100, transaction_type="d"
        )
        self.transaction2 = create_dummy_transaction(
            seller=self.seller, amount=50, transaction_type="w"
        )

        self.api_url = reverse("seller-transactions", args=[self.seller.id])

    @patch("credit_management.models.Seller.objects.get")
    def test_get_transactions_for_valid_seller(self, mock_get):
        """Test retrieving transactions for a valid seller."""
        mock_get.return_value = self.seller
        response = self.client.get(self.api_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["amount"], 100)
        self.assertEqual(response.data[0]["transaction_type"], "d")
        self.assertEqual(response.data[1]["amount"], 50)
        self.assertEqual(response.data[1]["transaction_type"], "w")

    @patch("credit_management.models.Seller.objects.get")
    def test_get_transactions_for_invalid_seller(self, mock_get):
        """Test retrieving transactions for an invalid seller."""
        mock_get.side_effect = Seller.DoesNotExist
        response = self.client.get(self.api_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Seller not found")
