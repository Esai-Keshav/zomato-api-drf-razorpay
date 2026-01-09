from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Allows access only to users who belong to the Customer group.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="customer").exists()
        )


class IsHotelOwner(BasePermission):
    """
    Allows access only to users who belong to the hotel_owner group.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="hotel_owner").exists()
        )


class IsDeliveryAgent(BasePermission):
    """
    Allows access only to users who belong to the hotel_owner group.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="delivery_agent").exists()
        )
