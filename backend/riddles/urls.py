from django.urls import path

from . import views

# Register your urls here.
urlpatterns = [
    path("users", views.get_users, name="users"),
    path("get-username/<int:player_id>", views.get_username, name="get_username"),
    # path("get-json", views.get_json, name="get_json"),
    path("get-hint", views.get_hint, name="get_hint"),
    path("server-mounted", views.server_mounted, name="server_mounted"),
    path("ips", views.get_all_ips, name="all_ips"),
    path("culprit", views.culprit, name="culprit"),
    path("leader-position", views.org_leader_position, name="org_leader_position"),
]

app_name = ""
