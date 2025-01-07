from django.test import TestCase
from _helper.tests.factory import (
    create_dummy_charge_request,
    create_dummy_seller,
    create_dummy_transaction,
)
from credit_management.models import Seller, Transaction, ChargeRequest
from django.core.exceptions import ValidationError


class TestTransaction(TestCase):
    def setUp(self):
        """create a seller with 10 credits to test."""
        self.seller = create_dummy_seller()
        self.charge_request = create_dummy_charge_request(seller=self.seller, amount=10)
        self.charge_request.is_accepted = True
        self.charge_request.save()

    def test_transaction_model(self):
        """Test logics about transaction model"""
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(self.seller.remain_balance, 10)

        # Add transaction for seller and check balance
        create_dummy_transaction(seller=self.seller, transaction_type="d", amount=20)
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertEqual(self.seller.remain_balance, 30)

        create_dummy_transaction(seller=self.seller, transaction_type="w", amount=5)
        self.assertEqual(Transaction.objects.count(), 3)
        self.assertEqual(self.seller.remain_balance, 25)

        # Check raise error if we have incorrect transaction_type
        transaction = create_dummy_transaction(
            seller=self.seller, transaction_type="c", amount=5
        )
        with self.assertRaises(ValidationError) as e:
            transaction.full_clean()
