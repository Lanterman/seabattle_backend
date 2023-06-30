from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMyProfile(BasePermission):
    """If my profile - everything is allowed, otherwise only reading"""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.username == obj.username
        )

class IsAccountOwner(BasePermission):
    """Allows the action only to the account owner"""

    message = "This action is only allowed for the account owner"

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
