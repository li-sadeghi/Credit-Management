from unittest import mock
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from credit_management.models import Seller
from _helper.tests.factory import (
    create_dummy_seller,
    create_dummy_charge_request,
    create_dummy_user,
)


class TransferViewTests(APITestCase):
    """Test suite for the Transfer view"""

    def setUp(self):
        """Set up test environment by creating dummy sellers, charge requests, and transfer URL."""
        self.user1 = create_dummy_user(username="test1", email="test1@gmail.com")
        self.user2 = create_dummy_user(username="test2", email="test2@gamil.com")
        self.seller1 = create_dummy_seller(
            full_name="seller1", phone_number="09345678907", user=self.user1
        )
        self.seller2 = create_dummy_seller(
            full_name="seller2", phone_number="09876543217", user=self.user2
        )

        seller1_charge = create_dummy_charge_request(seller=self.seller1, amount=1000)
        seller2_charge = create_dummy_charge_request(seller=self.seller2, amount=1000)

        seller1_charge.is_accepted = True
        seller2_charge.is_accepted = True
        seller1_charge.save()
        seller2_charge.save()

        self.url = reverse("transfer")
        self.client.login(username="test1", password=self.user1.raw_password)

    @mock.patch("credit_management.models.Transaction.objects.create")
    @mock.patch("credit_management.serializers.TransferSerializer.is_valid")
    @mock.patch("credit_management.serializers.TransferSerializer.validated_data")
    def test_transfer_between_valid_sellers_must_be_successed(
        self, mock_validated_data, mock_is_valid, mock_create
    ):
        """Test a successful transfer between valid sellers."""
        mock_validated_data.return_value = {
            "sender": self.seller1,
            "receiver": self.seller2,
            "amount": 200,
        }
        mock_is_valid.return_value = True
        mock_create.return_value = None

        data = {
            "receiver_phone": self.seller2.phone_number,
            "amount": 200,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Transfer successful."})

    @mock.patch("credit_management.serializers.TransferSerializer.validated_data")
    def test_transfer_between_invalid_sellers_must_be_failed(self, mock_validated_data):
        """Test a failed transfer between a valid and an invalid seller."""
        mock_validated_data.side_effect = Seller.DoesNotExist
        data = {
            "receiver_phone": "11111",
            "amount": 200,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_block_for_non_seller_user(self):
        """Test when a non seller user tried to transfer, block it by permission denied."""
        self.seller2.user = None
        self.seller2.save()
        self.client.login(username="test2", password=self.user2.raw_password)
        data = {
            "receiver_phone": self.seller1.phone_number,
            "amount": 200,
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_decrease_and_increase_of_remaining_balances_in_successful_transfer(self):
        """Test the balance update after a successful transfer."""
        data = {
            "receiver_phone": self.seller2.phone_number,
            "amount": 200,
        }
        response = self.client.post(self.url, data, format="json")
        self.seller1.refresh_from_db()
        self.seller2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.seller1.credit, 800)
        self.assertEqual(self.seller2.credit, 1200)

    def test_decrease_and_increase_of_remaining_balances_in_failed_transfer(self):
        """Test the balance remains unchanged after a failed transfer."""
        data = {
            "receiver_phone": "11111",
            "amount": 200,
        }
        response = self.client.post(self.url, data, format="json")
        self.seller1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.seller1.credit, 1000)

    def test_user_canont_charge_itself(self):
        """Test block users to charge for themselves."""
        # The user1 try to charge itself
        data = {
            "receiver_phone": self.seller1.phone_number,
            "amount": 200,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
