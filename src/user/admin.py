from gettext import ngettext
from django.contrib import messages
from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """Lobby admin"""

    list_display = (
        "id", "username", "first_name", "last_name", "email", "cash", "rating", "created_in", "is_active", 
        "is_staff", "photo"
    )
    list_display_links = ("id", "username", "first_name", "last_name")
    fields = (
        "username", "first_name", "last_name", "email", "mobile_number", "cash", "rating", "is_active", "is_staff",
        "updated_in", "hashed_password", "photo"
    )
    search_fields = ("username", "first_name", "last_name")
    list_filter = ("is_active", "is_staff")
    list_max_show_all = 250
    list_per_page = 150
    actions = ["activate_user", "deactivate_user", "grant_access_to_admin_site", "deny_access_to_admin_site"]

    @admin.action(description="Activate user(-s)")
    def activate_user(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, ngettext(
            '%d user was successfully activated.',
            '%d users were successfully activated.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Deactivate user(-s)")
    def deactivate_user(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, ngettext(
            '%d user was successfully activated.',
            '%d users were successfully activated.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Grant access to admin site")
    def grant_access_to_admin_site(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, ngettext(
            '%d user was successfully granted access to the admin site.',
            '%d users were successfully granted access to the admin site.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Deny access to admin site")
    def deny_access_to_admin_site(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, ngettext(
            '%d user was successfully denied access to the admin site.',
            '%d users were successfully denied access to the admin site.',
            updated,
        ) % updated, messages.SUCCESS)
