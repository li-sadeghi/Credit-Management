from django.test import TestCase
from _helper.tests.factory import (
    create_dummy_seller,
    create_dummy_transaction,
    create_dummy_charge_request,
)
from credit_management.models import Seller
from django.core.exceptions import ValidationError


class TestSeller(TestCase):
    def test_seller_model(self):
        """Test some logics for seller model that be sure work properly."""
        # Should not create a seller with wrong phone number format
        with self.assertRaises(ValidationError) as e:
            create_dummy_seller(phone_number="1234")

        # Create successfully a seller with name and phone number in correct formats
        seller = create_dummy_seller(
            full_name="Ali Sadeghi", phone_number="09103527237"
        )
        self.assertEqual(Seller.objects.count(), 1)
        self.assertEqual(seller.full_name, "Ali Sadeghi")
        self.assertEqual(seller.phone_number, "09103527237")
        self.assertEqual(seller.remain_balance, 0)
