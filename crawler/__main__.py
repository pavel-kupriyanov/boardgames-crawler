import asyncio
from argparse import ArgumentParser

import settings
from crawler.crawler_ import start_crawler

parser = ArgumentParser()

db_group = parser.add_argument_group('database', 'database connection settings')
db_settings = {
    'user': (settings.DB_NAME, str),
    'password': (settings.DB_PASSWORD, str),
    'host': (settings.DB_HOST, str),
    'port': (settings.DB_PORT, int),
    'name': (settings.DB_NAME, str)
}

for key, value in db_settings.items():
    db_group.add_argument(f'--db_{key}', help=f'Database {key}', default=value[0], type=value[1], required=False)

crawler_group = parser.add_argument_group('crawler', 'crawler settings')

# TODO add settings


def main():
    args = parser.parse_args()
    asyncio.run(start_crawler(args))


if __name__ == '__main__':
    main()
