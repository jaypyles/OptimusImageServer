import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Parameters for the request
authorization_code = os.getenv("CODE")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:3000"
refresh_token = os.getenv("REFRESH_TOKEN")

TOKEN_URL = "https://accounts.spotify.com/api/token"
basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()


def get_access_token():
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to obtain the access token. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None


NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"


def get_now_playing():
    access_token = get_access_token().get("access_token")

    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(NOW_PLAYING_URL, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to fetch currently playing. Status code: {response.status_code}"
            )
            print(f"Response: {response.text}")
            return None
    else:
        print("Access token not obtained.")
        return None


def now_playing():
    """Get and format Spotify now playing."""
    now = get_now_playing()
    return {
        "songName": now["item"]["name"],
        "albumName": now["item"]["album"]["name"],
        "artistName": now["item"]["artists"][0]["name"],
        "albumCover": now["item"]["album"]["images"][0]["url"],
    }
