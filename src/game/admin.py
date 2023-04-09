from gettext import ngettext
from django.contrib import admin, messages

from . import models


class ShipInlince(admin.TabularInline):
    """Options for inline editing of Ship `model` instances."""

    model = models.Ship
    extra = 4
    max_num = 4


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
    actions = ["delete_winner"]

    @admin.action(description="Delete winner")
    def delete_winner(self, request, queryset):
        updated = queryset.update(winner="", finished_in=None)
        self.message_user(request, ngettext(
            'Winner successfully removed from %d lobby.',
            'Winner successfully removed from %d lobbies.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    """Board admin"""

    list_display = ("id", "lobby_id", "user_id", "is_ready", "is_my_turn", "is_play_again")
    list_display_links = ("id", "lobby_id")
    fields = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "is_ready", "is_my_turn", "is_play_again", 
              "lobby_id", "user_id")
    search_fields = ("lobby_id", )
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True
    inlines = [ShipInlince]
    raw_id_fields = ("lobby_id", "user_id")
    actions = ["make_prepared", "make_unprepared", "clear_is_play_again_field", "clear_all_boolean_fields"]

    @admin.action(description="Make prepared")
    def make_prepared(self, request, queryset):
        updated = queryset.update(is_ready=True)
        self.message_user(request, ngettext(
            '%d board was successfully prepared.',
            '%d boards were successfully prepared.',
            updated,
        ) % updated, messages.SUCCESS)
    
    @admin.action(description="Make unprepared")
    def make_unprepared(self, request, queryset):
        updated = queryset.update(is_ready=False)
        self.message_user(request, ngettext(
            '%d board was successfully unprepared.',
            '%d boards were successfully unprepared.',
            updated,
        ) % updated, messages.SUCCESS)
    
    @admin.action(description="Clear an is_play_again field")
    def clear_is_play_again_field(self, request, queryset):
        updated = queryset.update(is_play_again=None)
        self.message_user(request, ngettext(
            'Сleared the is_play_again field on %d board.',
            'Сleared the is_play_again field on %d boards.',
            updated,
        ) % updated, messages.SUCCESS)
    
    @admin.action(description="Clear all boolean field")
    def clear_all_boolean_fields(self, request, queryset):
        updated = queryset.update(is_ready=False, is_my_turn=False, is_play_again=None)
        self.message_user(request, ngettext(
            'Сleared all boolean fields on %d board.',
            'Сleared all boolean fields on %d boards.',
            updated,
        ) % updated, messages.SUCCESS)


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


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """Ship admin"""

    list_display = ("id", "owner", "is_bot", "created_in", "lobby_id")
    list_display_links = ("id", "owner")
    fields = ("message", "owner", "is_bot", "lobby_id")
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True
    raw_id_fields = ("lobby_id", )
