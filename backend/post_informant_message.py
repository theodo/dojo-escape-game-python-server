import time

import requests


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BASE_URL = "http://localhost:8000"
SLEEP_TIMER = 20
ADMIN_SECRET = "the_killer_is_colonel_custard"
SPOTIFY_HINT = "ID DE PLAYLIST"
BASE_MESSAGE_CONTENT = """
Ok {}, j'ai des infos pour toi.
Un portable a été retrouvé sur une des scènes de crime.
Il était sous scellés au commissariat, mais il a disparu depuis quelques heures.
Le voleur a sûrement voulu effacer des preuves sur le téléphone, donc il a un lien avec les meurtres.
Heureusement, on avait mis un mouchard dessus qui a capté quelques octets de données.
Les données en arrière-plan, tout le monde oublie de les désactiver. Une chance pour nous !
On sait que la chaîne de caractère {} a été envoyé aux serveurs de Spotify.
Le voleur a sûrement un lien avec le(s) tueur(s). Retrouvez qui a utilisé le téléphone en retrouvant à quoi correspond {}.
"""

while True:
    ips = requests.get(f"{BASE_URL}/ips", headers={"Authorization": ADMIN_SECRET}, timeout=5).json()

    for username, ip in ips.items():
        print(f"Posting message to user {username} (IP : {ip})")
        try:
            response = requests.post(f"http://{ip}:8000", data=BASE_MESSAGE_CONTENT.format(username, SPOTIFY_HINT, SPOTIFY_HINT), timeout=3)
            assert response.status_code == 200
            print(colors.OKGREEN + f"Successfully posted message to user {username} (IP : {ip})" + colors.ENDC)
        except:
            print(colors.FAIL + f"Post has failed for user {username} (IP : {ip})" + colors.ENDC)
    time.sleep(SLEEP_TIMER)
