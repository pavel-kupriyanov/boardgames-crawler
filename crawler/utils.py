from settings import BASE_VERBOSE_URL


async def load_paginated_items(get_more, limit_on_page=100, stop_on=None):
    """
    Call get_more and return results one by one until we return <stop_on> items or get_more return []
    :param get_more: function with params limit and offset that return list of items
    :param limit: number of items in one page
    :param stop_on: number of item that we need or None if we need all
    :return: generator that returns items
    """
    buffer, offset = [], 0
    while stop_on is None or offset < stop_on:
        if not buffer:
            buffer = await get_more(limit_on_page, offset)
        if not buffer:
            raise StopAsyncIteration
        offset += 1
        yield buffer.pop(0)


def clear_category(category):
    return {'tesera_id': category.get('id'), 'name': category.get('name')}


def clear_game(game):
    return {
        'tesera_id': game.get('teseraId'),
        'name': game.get('title2') or game.get('title3') or game.get('title'),
        'en_name': game.get('title'),
        'description': game.get('descriptionShort') or game.get('description') or '',
        'photo': game.get('photoUrl'),
        'bgg_rating': game.get('bggRating'),
        'min_players': game.get('playersMin'),
        'min_players_recommended': game.get('playersMinRecommend'),
        'max_players': game.get('playersMax'),
        'max_players_recommended': game.get('playersMaxRecommend'),
        'play_time_min': game.get('playtimeMin'),
        'play_time_max': game.get('playtimeMax'),
        'tesera_url': BASE_VERBOSE_URL + 'game/' + game.get('alias'),
    }
