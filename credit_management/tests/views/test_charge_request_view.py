from rest_framework.test import APITestCase
from _helper.tests.factory import (
    create_dummy_seller,
    create_dummy_user,
)
from django.urls import reverse
from rest_framework import status


class TestChargeRequest(APITestCase):
    """Test cases for charge request creation api."""

    def setUp(self):
        """Sets up the initial test data.

        Creates a user and a seller associated with that user, then logs the user in.
        Sets the API URL for charge request creation.
        """
        self.user1 = create_dummy_user(username="test1")
        self.seller1 = create_dummy_seller(user=self.user1)

        self.api_url = reverse("charge-request-create")
        self.client.login(username="test1", password=self.user1.raw_password)

    def test_create_successfully_charge_request(self):
        """Test the successful creation of a charge request for a seller user."""
        data = {"amount": 2000}

        response = self.client.post(self.api_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_two_charge_request_for_one_seller_must_blocked(self):
        """Test that creating two charge requests for the same seller is blocked."""
        data = {"amount": 2000}
        self.client.post(self.api_url, data)

        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_non_seller_cannot_create_charge_request(self):
        """Test that a non-seller user cannot create a charge request."""
        user2 = create_dummy_user(username="test2")
        self.client.login(username="test2", password=user2.raw_password)
        data = {"amount": 2000}
        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
