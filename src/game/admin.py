from django.contrib import admin

from . import models


class BoardInlince(admin.TabularInline):
    model = models.Board


@admin.register(models.Lobby)
class LobbyAdmin(admin.ModelAdmin):
    """Lobby admin"""

    list_display = ("id", "name", "bet", "time_to_move", "time_to_placement", "winner", "created_in", "finished_in")
    list_display_links = ("id", "name")
    fields = ("name", "slug", "finished_in", "bet", "time_to_move", "time_to_placement", "password", "winner", "users")
    search_fields = ("name", )
    list_filter = ("bet", "time_to_move", "time_to_placement")
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True
    raw_id_fields = ("users", )


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    """Board admin"""

    list_display = ("id", "lobby_id", "user_id", "is_ready", "my_turn")
    list_display_links = ("id", )
    fields = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "is_ready", "my_turn", "lobby_id", "user_id")
    search_fields = ("lobby_id", )
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True
    raw_id_fields = ("lobby_id", "user_id")


@admin.register(models.Ship)
class ShipAdmin(admin.ModelAdmin):
    """Ship admin"""

    list_display = ("id", "name", "plane", "size", "count", "board_id")
    list_display_links = ("id", "name")
    fields = ("name", "plane", "size", "count", "board_id")
    search_fields = ("board_id", )
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True
    raw_id_fields = ("board_id", )


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    """Ship admin"""

    list_display = ("id", "lobby_slug")
    list_display_links = ("id", "lobby_slug")
    fields = ("lobby_slug", )
    list_max_show_all = 250
    list_per_page = 150


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """Ship admin"""

    list_display = ("id", "owner", "created_in", "chat_id")
    list_display_links = ("id", "owner")
    fields = ("message", "onwer", "chat_id")
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True
    raw_id_fields = ("chat_id", )
