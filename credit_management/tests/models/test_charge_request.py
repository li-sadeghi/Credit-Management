from django.test import TestCase
from credit_management.models import ChargeRequest, Transaction
from _helper.tests.factory import create_dummy_seller, create_dummy_charge_request


class TestChargeRequest(TestCase):
    def setUp(self):
        """create a seller and a charge request for testing charge request model."""
        self.seller = create_dummy_seller()
        self.charge_request = create_dummy_charge_request(
            seller=self.seller, amount=100
        )

    def test_charge_request_model(self):
        """Test some logics for charge request model."""
        # The default value of new charge request must be False
        self.assertFalse(self.charge_request.is_accepted)

        # When we accept the charge request, a transaction must create
        charge_request = ChargeRequest.objects.get(seller=self.seller)
        charge_request.is_accepted = True
        charge_request.save()
        self.assertEqual(Transaction.objects.count(), 1)

        # Check the remaining balance of seller
        self.assertEqual(self.seller.remain_balance, 100)
