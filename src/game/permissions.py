from rest_framework.permissions import BasePermission

from . import services


class IsLobbyFree(BasePermission):
    """Check if the lobby is free"""

    message = "The lobby is crowded"

    def has_object_permission(self, request, view, obj):
        return services.is_lobby_free(request.user, obj)
