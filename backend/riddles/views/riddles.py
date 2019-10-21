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
    users_with_ips = User.objects.filter(level=4).exclude(ip_address__isnull=True)
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
        "Detective {}, we received your message. You will hear from us shortly".format(
            user.username
        ),
        status=200,
    )


# Riddle 5
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def culprit(request):
    user = request.user
    data = request.data

    if user.level == 3:
        user.level = 4

    user.save()

    if data["culprit_name"].lower() == "jordan lao":
        return Response(
            "Détective {}, vous m'avez percé à jour. Ne me dénoncez pas s'il vous plaît ! En échange je suis prêt à dénoncer tous mes complices ! Tu peux récupérer la liste membres de l'organisation dans cette archive-là : {}. Pour ouvrir le fichier, tu peux utiliser le mot de passe suivant : {}".format(
                user.username, "7c98210e2cc.zip", "QuiPeutMeStopper77"
            ),
            status=200,
        )

    else:
        return Response(
            "Détective {}, vous vous êtes trompé. Je ne suis pas le coupable. NE ME TOUCHEZ PAS!".format(
                user.username
            ),
            status=400,
        )
