import threading
from django.db import transaction
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from _helper.tests.factory import (
    create_dummy_seller,
    create_dummy_charge_request,
    create_dummy_transaction,
    create_dummy_user,
)
from credit_management.models import Seller
from django.db import connection


class TestTransaction(TransactionTestCase):
    """Test cases for simulating race conditions in transactions."""

    def setUp(self):
        """Set up initial test data for sellers and transaction URLs."""
        self.client = APIClient()
        self.user1 = create_dummy_user(username="test1")
        self.seller1 = create_dummy_seller(
            full_name="seller1", phone_number="09345678907", user=self.user1
        )
        self.seller2 = create_dummy_seller(
            full_name="seller2", phone_number="09876543217"
        )

        with transaction.atomic():
            seller1_charge = create_dummy_charge_request(
                seller=self.seller1, amount=1000
            )
            seller2_charge = create_dummy_charge_request(
                seller=self.seller2, amount=1000
            )

            seller1_charge.is_accepted = True
            seller2_charge.is_accepted = True
            seller1_charge.save()
            seller2_charge.save()

        self.url = reverse("transfer")
        self.client.login(username="test1", password=self.user1.raw_password)

    def test_transfer_race_condition(self):
        """Test transfer api for race conditions."""

        def _make_request():
            """Helper function to make a transfer request."""
            data = {
                "sender_phone": self.seller1.phone_number,
                "receiver_phone": self.seller2.phone_number,
                "amount": 100,
            }
            response = self.client.post(self.url, data, format="json")
            connection.close()

        threads = []
        for _ in range(10):
            thread = threading.Thread(target=_make_request)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        seller1 = Seller.objects.get(id=self.seller1.id)
        seller2 = Seller.objects.get(id=self.seller2.id)
        self.assertEqual(seller1.credit, 0)
        self.assertEqual(seller2.credit, 2000)

    def test_transaction_model_race_condition(self):
        """Test transaction model handling under race conditions."""

        def _make_transaction():
            """Helper function to create transactions."""
            create_dummy_transaction(
                seller=self.seller1, transaction_type="d", amount=10
            )
            create_dummy_transaction(
                seller=self.seller2, transaction_type="w", amount=10
            )
            connection.close()

        threads = []
        for _ in range(10):
            thread = threading.Thread(target=_make_transaction)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        seller1 = Seller.objects.get(id=self.seller1.id)
        seller2 = Seller.objects.get(id=self.seller2.id)
        self.assertEqual(seller1.credit, 1100)
        self.assertEqual(seller2.credit, 900)
