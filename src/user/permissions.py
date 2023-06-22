from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMyProfile(BasePermission):
    """If my profile - everything is allowed, otherwise only reading"""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.username == obj.username
        )