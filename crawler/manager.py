import asyncio
from enum import Enum

from db.functions import get_pool, clear_category, clear_game
from db import queries


class Table(Enum):
    Category = 1
    Game = 2
    ManyToMany = 3


class DatabaseManager:
    """
    This class monitors the records that already in the database, gets the records loaded by the crawler,
    determines whether to write data to the database.
    """

    get_queries = {
        Table.Category: queries.get_categories,
        Table.Game: queries.get_games,
        Table.ManyToMany: queries.get_mtm,
    }

    def __init__(self, db_url):
        self.db_ids = {key: set() for key in self.get_queries.keys()}
        self.temp_data = {key: dict() for key in self.get_queries.keys()}
        self.db_url = db_url
        self.pool = None

    async def load_from_db(self):
        self.pool = await get_pool(self.db_url)
        await asyncio.gather(*(self._get_data(table) for table in self.get_queries.keys()))

    async def _get_data(self, table):
        query = self.get_queries[table]
        columns = ('game_category_id', 'game_id') if table is Table.ManyToMany else ('tesera_id',)
        async with self.pool.acquire() as con:
            records = await con.fetch(query(columns))
        ids = (record[column] for column in columns for record in records)
        self.db_ids[table].update(ids)

    async def add_categories(self, categories):
        filtered_categories = [clear_category(category) for category in categories if
                               category['id'] not in self.db_ids[Table.Category]]
        if not filtered_categories:
            return
        query = queries.add_categories(filtered_categories)
        async with self.pool.acquire() as con:
            await con.execute(query)
        self.db_ids[Table.Category].update([category['tesera_id'] for category in categories])

    # async def add_game(self, game, category):
    #     game = clear_game(game)
    #     tesera_id = game['tesera_id']
    #
    #     if tesera_id in self.db_ids[Table.Game] or tesera_id in self.temp_data[Table.Game].keys():
    #         return
