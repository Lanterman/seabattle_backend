from rest_framework.permissions import BasePermission

from . import services


class IsLobbyFree(BasePermission):
    """Check if the lobby is free"""

    message = "The lobby is crowded"

    def has_object_permission(self, request, view, obj):
        if len(obj.users.all()) < 2 or request.user in obj.users.all():
            return True
        return False
