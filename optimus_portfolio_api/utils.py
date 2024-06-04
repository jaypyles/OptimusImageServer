# STL
import os
import base64
import logging

# PDM
import requests
from dotenv import load_dotenv

_ = load_dotenv()

# Parameters for the request
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

TOKEN_URL = "https://accounts.spotify.com/api/token"
basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

LOG = logging.getLogger(__name__)


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
    print(now)
    return {
        "songName": now["item"]["name"],
        "songURL": now["item"]["external_urls"]["spotify"],
        "albumName": now["item"]["album"]["name"],
        "artistName": now["item"]["artists"][0]["name"],
        "albumCover": now["item"]["album"]["images"][0]["url"],
    }
