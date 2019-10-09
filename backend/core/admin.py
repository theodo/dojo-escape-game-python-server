from core.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("level", "player_id", "hint")}),
    ) + UserAdmin.fieldsets


admin.site.register(User, CustomUserAdmin)
