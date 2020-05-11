from functools import partial

import aiohttp

from crawler.utils import load_paginated_items
from crawler.requests import get_boardgames, get_categories
from crawler.manager import DatabaseManager

from db.schema import db_url
from db.functions import clear_category
import db.queries as queries


async def start_crawler(args):
    manager = DatabaseManager(db_url)
    await manager.load_from_db()
    async with aiohttp.ClientSession() as session:
        categories = await get_categories(session)
        await manager.add_categories(categories)
    #     cleared_categories = [clear_category(category) for category in categories]
    #     # query = queries.add_categories(cleared_categories)
    #     print(queries.get_categories(('tesera_id',)))
    #     # get_boardgames_partial = partial(get_boardgames, session)
    #     # boardgames_generator = load_paginated_items(get_boardgames_partial, 4, 4)
    #     # async for boardgame in boardgames_generator:
    #     #     print(boardgame)
