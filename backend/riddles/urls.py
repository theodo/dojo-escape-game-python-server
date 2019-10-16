from django.urls import path

from . import views

# Register your urls here.
urlpatterns = [
    path("users", views.get_users, name="users"),
    path("upgrade-to-level-1", views.upgrade_to_level_1, name="upgrade_to_level_1"),
    path("get-username/<int:player_id>", views.get_username, name="get_username"),
    path("get-json", views.get_json, name="get_json"),
    path("get-hint", views.get_hint, name="get_hint"),
    path("server-mounted", views.server_mounted, name="server_mounted"),
]

app_name = ""
