import json
import logging

import aiohttp

from settings import BASE_URL

OK = 200


async def _get_items(url: str, session: aiohttp.ClientSession, params: dict):
    async with session.get(url, params=params) as response:
        if response.status != OK:
            logging.warning(f"Response code {response.status}.")
            raise aiohttp.ClientConnectionError(f"Invalid status code {response.status}")
        return json.loads(await response.text())


async def get_boardgames(session: aiohttp.ClientSession, limit: int = 100, offset: int = 0, tags: int = None) -> dict:
    params = {'limit': limit, 'offset': offset, 'tags': tags}
    return await _get_items(BASE_URL + 'games', session, params)


async def get_categories(session: aiohttp.ClientSession,  limit: int = 100, offset: int = 0) -> dict:
    params = {'limit': limit, 'offset': offset}
    return await _get_items(BASE_URL + 'tags/types', session, params)
