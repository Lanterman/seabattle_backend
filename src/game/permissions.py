from rest_framework.permissions import BasePermission


class IsLobbyFree(BasePermission):
    """Check if the lobby is free"""

    message = "The lobby is crowded"

    def has_object_permission(self, request, view, obj):
        if len(obj.users.all()) < 2 or request.user in obj.users.all():
            return True
        return False


class IsPlayWithBot(BasePermission):
    """Check if the game with a bot"""

    message = "The lobby doesn't exists!"

    def has_object_permission(self, request, view, obj):
        if obj.is_play_with_a_bot:
            if request.user in obj.users.all():
                return True
        else:
            return True
        return False


class IsEnoughMoney(BasePermission):
    """Check if user enough money for the game"""

    message = "You don't have enough money to play"

    def has_object_permission(self, request, view, obj):
        if request.user.cash >= obj.bet:
            return True
        return False
