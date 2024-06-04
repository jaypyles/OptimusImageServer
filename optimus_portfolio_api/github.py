# STL
from typing import TypedDict
from datetime import datetime

# PDM
import requests


class GithubResponse(TypedDict):
    pushed_at: datetime
    html_url: str


def get_most_recent_public_project(username: str) -> str | None:
    url = f"https://api.github.com/users/{username}/repos?sort=updated"
    response = requests.get(url)

    if response.status_code == 200:
        repos: list[GithubResponse] = response.json()
        sorted_repos: list[GithubResponse] = sorted(repos, key=lambda d: d["pushed_at"])

        if repos:
            return sorted_repos[-1]["html_url"]

    else:
        return None
