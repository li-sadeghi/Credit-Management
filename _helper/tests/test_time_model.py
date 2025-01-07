"""
Test class for validating time-related functionality in the Seller model.

This test class utilizes the unittest framework and the freezegun library to ensure that time-related operations in the
Seller model function as expected.

- The `setUp` method freezes time to '2024-01-01' and initializes an Seller instance for testing.
- The `test_time_model` method checks the behavior of timestamps during creation, modification, and saving.
  - It asserts that both the creation and modification timestamps are initially set to the frozen time.
  - It updates the seller's name, saves the changes, and asserts that the creation timestamp remains unchanged.
  - Finally, it verifies that the modified timestamp reflects the current time after the save operation.

Note: The `create_dummy_seller` method from the '_helper' module is assumed to correctly create Seller instances
for testing purposes.

This test suite helps ensure the proper functioning of time-related features in the Seller model, providing
confidence in the reliability and accuracy of the model's temporal behavior.
"""

from datetime import datetime

from django.test import TestCase
from freezegun import freeze_time

from _helper.tests.factory import create_dummy_seller
from credit_management.models import Seller


class TestTimeModel(TestCase):
    @freeze_time("2024-01-01")
    def setUp(self) -> None:
        """
        Set up the test environment by freezing time and creating an Seller instance.
        """
        self.seller: Seller = create_dummy_seller("Ali Sadeghi", "09103527237")

    def test_time_model(self) -> None:
        """
        Test the time-related functionality of the Seller model.
        """
        # Assert that both the creation and modification timestamps are initially set to the frozen time
        self.assertEqual(self.seller.created.strftime("%Y-%m-%d"), "2024-01-01")
        self.assertEqual(self.seller.modified.strftime("%Y-%m-%d"), "2024-01-01")

        # Update the seller's full name and save changes
        self.seller.full_name = "test testian"
        self.seller.save()

        # Assert that the creation timestamp remains unchanged
        self.assertEqual(self.seller.created.strftime("%Y-%m-%d"), "2024-01-01")

        # Verify that the modified timestamp reflects the current time after the save operation
        self.assertEqual(
            self.seller.modified.strftime("%Y-%m-%d"),
            datetime.now().strftime("%Y-%m-%d"),
        )
