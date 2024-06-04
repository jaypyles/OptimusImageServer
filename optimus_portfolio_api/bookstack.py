# STL
import os
import json
from enum import Enum
from typing import TypedDict

# PDM
import urllib3

BOOKSTACK_TOKEN_ID = os.environ["BOOKSTACK_TOKEN_ID"]
BOOKSTACK_TOKEN_SECRET = os.environ["BOOKSTACK_TOKEN_SECRET"]
BOOKSTACK_BASE_URL = os.environ["BOOKSTACK_BASE_URL"]


assert BOOKSTACK_TOKEN_ID
assert BOOKSTACK_TOKEN_SECRET
assert BOOKSTACK_BASE_URL


class BookstackAPIEndpoints(Enum):
    PAGES = "/api/pages"


class RequestType(Enum):
    POST = "POST"
    GET = "GET"


class BookstackValue(TypedDict):
    updated_at: str
    book_slug: str
    slug: str


class BookstackClient:
    def __init__(self) -> None:
        self.id = BOOKSTACK_TOKEN_ID
        self.secret = BOOKSTACK_TOKEN_SECRET
        self.headers = {"Authorization": f"Token {self.id}:{self.secret}"}
        self.http = urllib3.PoolManager()

    def _make_request(
        self, request_type: RequestType, endpoint: BookstackAPIEndpoints
    ) -> urllib3.BaseHTTPResponse:
        request_url = BOOKSTACK_BASE_URL + endpoint.value
        resp = self.http.request(request_type.value, request_url, headers=self.headers)
        return resp

    def get_pages(self) -> list[BookstackValue]:
        """Get Bookstack's pages from the Client"""
        resp = self._make_request(RequestType.GET, BookstackAPIEndpoints.PAGES)
        assert resp

        class BookstackResponse(TypedDict):
            data: list[BookstackValue]

        data: BookstackResponse = json.loads(resp.data.decode())
        return data["data"]


if __name__ == "__main__":
    b = BookstackClient()
    pages = b.get_pages()
    print(pages)
