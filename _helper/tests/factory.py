from credit_management.models import Seller, ChargeRequest, Transaction


def create_dummy_seller(
    full_name: str = "Ali Mamadi", phone_number: str = "09123456789"
) -> Seller:
    """Creates and returns a dummy seller."""
    return Seller.objects.create(full_name=full_name, phone_number=phone_number)


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
