from sqlalchemy.dialects import postgresql

from .schema import Category, Game, ManyToMany


def compiled_with_table(model):
    def compiled(func):
        def wrapper(*args, **kwargs):
            query = func(model.__table__, *args, **kwargs)
            query = query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
            return str(query)

        return wrapper

    return compiled


@compiled_with_table(Category)
def add_categories(table, categories):
    return _add(table, categories)


@compiled_with_table(Game)
def add_games(table, games):
    return _add(table, games)


@compiled_with_table(ManyToMany)
def add_mtm(table, mtm):
    return _add(table, mtm)


@compiled_with_table(Category)
def get_categories(table, fields: tuple = None):
    return _get(table, fields)


@compiled_with_table(Game)
def get_games(table, fields: tuple = None):
    return _get(table, fields)


@compiled_with_table(ManyToMany)
def get_mtm(table, fields: tuple = None):
    return _get(table, fields)


def _get(table, fields: tuple = None):
    select = table.select()
    if fields:
        return select.with_only_columns([table.columns[field] for field in fields])
    return select


def _add(table, data):
    return table.insert().values(tuple(data))
