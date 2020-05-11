import asyncpg


async def get_pool(db_url):
    return await asyncpg.create_pool(db_url)


def clear_category(category):
    return {'tesera_id': category.get('id'), 'name': category.get('name')}


def clear_game(game):
    return {}
