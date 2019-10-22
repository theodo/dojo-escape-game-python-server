from core.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "level",
                    "player_id",
                    "hint",
                    "ip_address",
                    "server_mounted",
                    "hint_color",
                    "hint_location",
                    "explicit_password",
                )
            },
        ),
    ) + UserAdmin.fieldsets

    list_display = (
        "id",
        "username",
        "explicit_password",
        "hint_color",
        "hint_location",
        "is_staff",
    )


admin.site.register(User, CustomUserAdmin)
