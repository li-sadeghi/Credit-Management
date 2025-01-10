from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    """
    Custom permission to allow access only to users associated with a Seller instance.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and associated with a Seller
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "seller")
        )
