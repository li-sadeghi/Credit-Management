from credit_management.models import Seller, ChargeRequest, Transaction
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import random
import string


def create_dummy_seller(
    full_name: str = "Ali Mamadi", phone_number: str = "09123456789", user: User = None
) -> Seller:
    """Creates and returns a dummy seller."""
    return Seller.objects.create(
        full_name=full_name, phone_number=phone_number, user=user
    )


def create_dummy_charge_request(seller: Seller, amount: int, **kwargs) -> ChargeRequest:
    """Creates and returns a dummy charge request for a seller."""
    return ChargeRequest.objects.create(seller=seller, amount=amount, **kwargs)


def create_dummy_transaction(
    seller: Seller, transaction_type: str, amount: int
) -> Transaction:
    """Creates and returns a dummy transaction for a seller."""
    return Transaction.objects.create(
        seller=seller, transaction_type=transaction_type, amount=amount
    )


def create_dummy_user(**kwargs) -> User:
    """Create and return a dummy user with random values for its username and password."""
    kwargs.setdefault(
        "username",
        "test_user" + "".join(random.choice(string.ascii_letters) for i in range(8)),
    )
    kwargs.setdefault("password", "F4kePaSs0d")
    kwargs.setdefault("email", "test_user@example.com")
    user = User.objects.create_user(**kwargs)
    user.raw_password = kwargs["password"]
    return user
