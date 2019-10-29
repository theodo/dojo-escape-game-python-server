import random

import jwt
from core.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

SECRET = "MY_AWESOME_SECRET"
ADMIN_SECRET = "the_killer_is_colonel_custard"


# Riddle 1
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
        user.level = 0
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


# Riddle 2
@api_view(["GET"])
def get_hint(request):
    token = request.GET.get("token", "")
    data = jwt.decode(token, SECRET, algorithms=["HS256"])
    try:
        user = User.objects.get(player_id=data["player_id"], username=data["username"])
        if user.level == 0:
            user.level = 1
            user.save()

        return Response(user.hint, status=200)
    except User.DoesNotExist:
        return Response({}, status=400)


@api_view(["GET"])
def get_all_ips(request):
    token = request.headers.get("Authorization")
    if token != ADMIN_SECRET:
        return Response(status=404)
    users_with_ips = User.objects.filter(level=3).exclude(ip_address__isnull=True)
    return Response(
        {user.username: user.ip_address for user in users_with_ips}, status=200
    )


# Riddle 4
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def server_mounted(request):
    user = request.user
    data = request.data

    user.ip_address = data["ip_address"]
    user.server_mounted = True

    if user.level == 2:
        user.level = 3

    user.save()

    return Response(
        f"Détective {user.username}, nous avons reçu votre message. Veuillez patienter, nous allons vous briefer sur votre mission",
        status=200,
    )


# Riddle 5
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def culprit(request):
    user = request.user
    data = request.data

    if data["culprit_name"].lower() == "jordan lao":

        if user.level == 3:
            user.level = 4
            user.save()

        archive_name = "7c98210e2cc.zip"
        archive_password = "QuiPeutMeStopper77"
        return Response(
            f"Détective {user.username}, tu m'as percé à jour. Ne me dénonce pas s'il te plaît ! En échange je suis prêt à dénoncer tous mes complices ! Tu peux récupérer des données sensibles sur l'organisation dans cette archive : {archive_name}. Pour ouvrir le fichier, tu peux utiliser le mot de passe suivant : {archive_password}",
            status=200,
        )

    else:
        return Response(
            f"Détective {user.username}, vous vous êtes trompé. Nous avons vérifié, ce n'est pas le coupable",
            status=400,
        )


# Riddle 6
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def org_leader_position(request):
    user = request.user
    data = request.data

    LEADER_LATITUDE = 40.8814439
    LEADER_LONGITUDE = 14.2947099
    try:
        sumbitted_latitude = float(data['latitude'])
        sumbitted_longitude = float(data['longitude'])
    except:
        return Response(
            {
                "message": "Ça ne ressemble pas à des coordonnées que nos drones peuvent exploiter...",
                "format_attendu": {"latitude": 12.1234567, "longitude": 12.1234567}
            },
            status=400
        )

    if sumbitted_latitude == LEADER_LATITUDE and sumbitted_longitude == LEADER_LONGITUDE:

        if user.level == 4:
            user.level = 5
            user.save()

        return Response(
            "Et merde, il est à l'aéroport! On contacte immédiatement nos collègues italiens. " +
            f"Il faut annuler tous les vols au départ de Naples! Merci pour le tuyau détective{user.username}. " +
            "Cette fois-ci on le tient ce fumier !",
            status=200,
        )

    else:
        return Response(
            "On a regardé les images du drone, mais il n'est pas là. " +
            f"Je crois que vous n'avez pas récupéré les bonnes coordonnées, détective {user.username}. ",
            status=404,
        )
