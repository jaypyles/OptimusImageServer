import asyncio
import os
from enum import Enum
from pprint import pprint

import notion_client

NOTION_DB_ID = os.environ["NOTION_DB_ID"]


class ProjectType(Enum):
    READY = "ready_for_development"
    DEV = "in_development"


NOTION_QUERY_MAP = {
    ProjectType.READY: {
        "database_id": NOTION_DB_ID,
        "filter": {
            "property": "Status",
            "status": {
                "equals": "Ready for Development",
            },
        },
    },
    ProjectType.DEV: {
        "database_id": NOTION_DB_ID,
        "filter": {
            "property": "Status",
            "status": {
                "equals": "In development",
            },
        },
    },
}


async def query(notion_secret: str, project_type: ProjectType):
    """Query projects in the Project Tracker in Notion"""
    notion = notion_client.AsyncClient(auth=notion_secret)
    query = NOTION_QUERY_MAP[project_type]

    notion_pages = []
    if pages := await notion.databases.query(**query):
        page_results = pages["results"]
        for result in page_results:
            properties = result["properties"]
            title = properties["Name"]["title"][0]["plain_text"]
            description = properties["Description"]["rich_text"]
            if description:
                description = description[0]["plain_text"]

            link = properties["Link"]["url"]
            project = properties["Type"]["rich_text"][0]["plain_text"]

            notion_pages.append(
                {
                    "title": title,
                    "description": description,
                    "link": link,
                    "project": project,
                }
            )

    return notion_pages


async def query_ready(notion_secret: str):
    return await query(notion_secret, ProjectType.READY)


async def query_dev(notion_secret: str):
    return await query(notion_secret, ProjectType.DEV)


async def main():
    NOTION_SECRET = os.environ["NOTION_SECRET"]
    await query_ready(NOTION_SECRET)
    await query_dev(NOTION_SECRET)


if __name__ == "__main__":
    asyncio.run(main())
