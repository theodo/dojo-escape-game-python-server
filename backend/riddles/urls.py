from django.urls import path

from . import views

# Register your urls here.
urlpatterns = [
    path("users/", views.get_users, name="users"),
    path("upgrade-to-level-1/", views.upgrade_to_level_1, name="upgrade_to_level_1"),
    path("get-username/<int:player_id>/", views.get_username, name="get_username"),
    path("get-json/", views.get_json, name="get_json"),
]

app_name = ""
