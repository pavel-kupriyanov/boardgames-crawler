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
