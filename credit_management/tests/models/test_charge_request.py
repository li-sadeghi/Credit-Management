from django.test import TestCase
from credit_management.models import ChargeRequest, Transaction
from _helper.tests.factory import create_dummy_seller, create_dummy_charge_request
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class TestChargeRequest(TestCase):
    def setUp(self):
        """create a seller for testing charge request model."""
        self.seller = create_dummy_seller()

    def test_charge_request_model(self):
        """Test some logics for charge request model."""
        charge_request = create_dummy_charge_request(seller=self.seller, amount=100)
        # The default value of new charge request must be False
        self.assertFalse(charge_request.is_accepted)

        # When we accept the charge request, credit of seller must be updated
        charge_request = ChargeRequest.objects.get(seller=self.seller)
        charge_request.is_accepted = True
        charge_request.save()
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 100)

    def test_uninqueness_of_charge_request_per_seller(self):
        """Test uninqueness logics of the charge request model."""
        # We can not create a charge request with accept=True.
        with self.assertRaises(ValidationError):
            create_dummy_charge_request(seller=self.seller, amount=10, is_accepted=True)

        # We can not have two charge request for a seller.
        create_dummy_charge_request(seller=self.seller, amount=10)
        with self.assertRaises(IntegrityError):
            create_dummy_charge_request(seller=self.seller, amount=10)
