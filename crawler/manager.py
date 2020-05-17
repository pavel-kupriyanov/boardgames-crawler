import asyncio
from enum import Enum

from db.schema import get_pool
from db import queries

from crawler.utils import clear_category, clear_game


class Table(Enum):
    Category = 1
    Game = 2
    ManyToMany = 3


class BaseDatabaseManager:
    """
    This class monitors the records that already in the database, gets the records loaded by the crawler,
    determines whether to write data to the database.
    """
    base_columns = None
    tables = ()
    reading_queries = {}
    writing_queries = {}

    def __init__(self, db_url):
        self.db_url = db_url
        self.pool = None
        self.db_ids = {key: set() for key in self.tables}
        self.temp_data = {key: dict() for key in self.tables}

    async def load_from_db(self):
        self.pool = await get_pool(self.db_url)
        await asyncio.gather(*(self._get_data(table) for table in self.tables))

    async def _get_data(self, table, columns=None):
        query = self.reading_queries[table]
        records = await self.fetch(query(columns))
        ids = (tuple(record[column] for column in columns) for record in records)
        ids = (id[0] if len(id) == 1 else id for id in ids)
        self.db_ids[table].update(ids)

    async def fetch(self, query):
        async with self.pool.acquire() as con:
            return await con.fetch(query)

    async def execute(self, query):
        async with self.pool.acquire() as con:
            await con.execute(query)

    async def flush(self, table):
        temp, ids = self.temp_data[table], self.db_ids[table]
        query = self.writing_queries[table]
        if temp.keys():
            await self.execute(query(temp.values()))
            ids.update(temp.keys())
            temp.clear()

    async def flush_all(self):
        await asyncio.gather(self.flush(table) for table in self.tables)


class BoardgamesManager(BaseDatabaseManager):
    base_columns = ('tesera_id',)
    tables = (Table.Category, Table.Game, Table.ManyToMany)

    reading_queries = {
        Table.Category: queries.get_categories,
        Table.Game: queries.get_games,
        Table.ManyToMany: queries.get_mtm,
    }

    writing_queries = {
        Table.Category: queries.add_categories,
        Table.Game: queries.add_games,
        Table.ManyToMany: queries.add_mtm,
    }

    def __init__(self, db_url, flush_after=100):
        super().__init__(db_url)
        self.temp_data[Table.ManyToMany] = set()
        self.flush_after = flush_after

    @property
    def categories(self):
        return list(self.db_ids[Table.Category])

    async def _get_data(self, table, columns=None):
        if columns is None:
            columns = ('game_category_tesera_id', 'game_tesera_id') if table is Table.ManyToMany else self.base_columns
        await super()._get_data(table, columns)

    async def _flush_mtm(self):
        temp, ids = self.temp_data[Table.ManyToMany], self.db_ids[Table.ManyToMany]
        # first we need filter mtm that games or categories not in db yet
        await self.load_from_db()
        mtm_to_write = []
        for mtm in temp:
            category_id, game_id = mtm
            foreign_in_db = category_id in self.db_ids[Table.Category] and game_id in self.db_ids[Table.Game]
            mtm_not_added = mtm not in ids
            if foreign_in_db and mtm_not_added:
                mtm_to_write.append({'game_category_tesera_id': category_id, 'game_tesera_id': game_id})

        if not mtm_to_write:
            return

        query = self.writing_queries[Table.ManyToMany]
        await self.execute(query(mtm_to_write))
        temp.clear()

    async def add_categories(self, categories):
        temp, ids = self.temp_data[Table.Category], self.db_ids[Table.Category]
        filtered_categories = [clear_category(cat) for cat in categories if cat['id'] not in ids]

        if not filtered_categories:
            return

        temp.update({cat['tesera_id']: cat for cat in filtered_categories})
        await self.flush(Table.Category)

    async def add_game(self, game):
        temp, ids = self.temp_data[Table.Game], self.db_ids[Table.Game]
        tesera_id = game['tesera_id']

        if tesera_id in temp.keys() or tesera_id in ids:
            # already added
            return

        temp[tesera_id] = game
        if len(temp) >= self.flush_after:
            await self.flush(Table.Game)

    async def add_mtm(self, game, category_id):
        temp, ids = self.temp_data[Table.ManyToMany], self.db_ids[Table.ManyToMany]
        mtm = (category_id, game['tesera_id'])
        if mtm in temp or mtm in ids:
            # already added
            return
        temp.add(mtm)
        if len(temp) >= self.flush_after:
            await self._flush_mtm()

    async def add_game_and_mtm(self, game, category):
        game = clear_game(game)
        await asyncio.gather(self.add_game(game), self.add_mtm(game, category))

    async def flush_all(self):
        await asyncio.gather(self.flush(Table.Category), self.flush(Table.Game))
        await self._flush_mtm()
