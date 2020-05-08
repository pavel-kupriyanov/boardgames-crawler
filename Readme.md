### Скрипт для получения информации о настольных играх с сайта tesera.ru.
Tesera API - https://api.tesera.ru/help/index.html

#### Установка

1. `git clone https://github.com/pavel-kupriyanov/boardgames-crawler.git`
2. `pip3 install -r requirements.txt`
3. Создать файл settings.py (смотри settings.example.py для примера)


#### Миграции

1. `cd db`
2. `alembic revision --message='Initial' --autogenerate`
3. `alembic upgrade head`


