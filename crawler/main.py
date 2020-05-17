from functools import partial

from aiohttp import ClientSession

from crawler.utils import load_paginated_items
from crawler.requests import get_boardgames, get_categories
from crawler.manager import BoardgamesManager

from db.schema import db_url


async def start_crawler(args):
    manager = BoardgamesManager(db_url)
    await manager.load_from_db()
    async with ClientSession() as session:
        categories = await get_categories(session)
        await manager.add_categories(categories)
        category = manager.categories[0]
        get_boardgames_partial = partial(get_boardgames, session, tags=category)
        boardgames_generator = load_paginated_items(get_boardgames_partial, 4, 4)
        async for boardgame in boardgames_generator:
            print(boardgame)
            await manager.add_game_and_mtm(boardgame, category)
        await manager.flush_all()
