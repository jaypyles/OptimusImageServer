import requests


def get_most_recent_public_project(username: str):
    url = f"https://api.github.com/users/{username}/repos?sort=updated"
    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json()
        if repos:
            return repos[0]["html_url"]
        else:
            return None
    else:
        return None
