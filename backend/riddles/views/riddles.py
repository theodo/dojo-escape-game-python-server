import random

import jwt
from core.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

SECRET = "MY_AWESOME_SECRET"
ADMIN_SECRET = "the_killer_is_colonel_custard"

@api_view(["POST"])
def upgrade_to_level_1(request):
    data = request.data
    try:
        username = data["username"]
    except KeyError:
        return Response({}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({}, status=404)

    user.level = 1
    user.save()

    return Response({}, status=200)


@api_view(["GET"])
def get_username(request, player_id):
    try:
        user = User.objects.get(player_id=player_id)
        return Response(user.username, status=200)
    except User.DoesNotExist:
        free_users = User.objects.filter(player_id=None, is_staff=False)
        user_index = random.randint(0, len(free_users))
        user = free_users[user_index]
        user.player_id = player_id
        user.save()

        return Response(user.username, status=200)


@api_view(["GET"])
def get_json(request):
    users = User.objects.filter(is_staff=False)
    response = {}
    for user in users:
        username = user.username
        for i in range(10000):
            token = jwt.encode(
                {"player_id": i, "username": username}, SECRET, algorithm="HS256"
            )
            response[
                f"{username}-{i}"
            ] = f"{request.build_absolute_uri('/api/get-hint')}?token={token.decode('ascii')}"  # .decode is needed because py-jwt return a binary string
    return Response(response, status=200)


@api_view(["GET"])
def get_hint(request):
    token = request.GET.get("token", "")
    data = jwt.decode(token, SECRET, algorithms=["HS256"])
    try:
        user = User.objects.get(player_id=data["player_id"], username=data["username"])
        return Response(user.hint, status=200)
    except User.DoesNotExist:
        return Response({}, status=400)


@api_view(["GET"])
def get_all_ips(request):
    token = request.headers.get("Authorization")
    if token != ADMIN_SECRET:
        return Response(status=404)
    users_with_ips = User.objects.filter(level=4).exclude(ip_address__isnull=True)
    return Response({user.username : user.ip_address for user in users_with_ips}, status=200)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def server_mounted(request):
    user = request.user
    data = request.data

    user.ip_address = data["ip_address"]
    user.server_mounted = True
    user.save()

    return Response(
        "Detective {}, we received your message. You will hear from us shortly".format(
            user.username
        ),
        status=200,
    )
