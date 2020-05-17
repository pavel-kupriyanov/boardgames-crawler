import asyncpg
from sqlalchemy import MetaData, Column, ForeignKey, Integer, SmallInteger, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

metadata = MetaData()

db_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

Base = declarative_base(metadata=metadata)


async def get_pool(db_url):
    return await asyncpg.create_pool(db_url)


class ManyToMany(Base):
    __tablename__ = 'category_game_mtm'
    __table_args__ = (UniqueConstraint('game_category_tesera_id', 'game_tesera_id'),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_category_tesera_id = Column('game_category_tesera_id', Integer, ForeignKey('game_category.tesera_id'))
    game_tesera_id = Column('game_tesera_id', Integer, ForeignKey('game.tesera_id'))


class Category(Base):
    __tablename__ = 'game_category'
    id = Column(Integer, primary_key=True)
    tesera_id = Column(Integer, unique=True)
    name = Column(String(100), unique=True)
    children = relationship("Game", secondary=ManyToMany.__table__)


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    tesera_id = Column(Integer, unique=True)
    name = Column(String(250), unique=True)
    en_name = Column(String(250), unique=True)
    description = Column(String(), nullable=True)
    photo = Column(String(), nullable=True)
    bgg_rating = Column(Float, default=0, nullable=True)
    min_players = Column(SmallInteger, default=2, nullable=True)
    min_players_recommended = Column(SmallInteger, default=2, nullable=True)
    max_players = Column(SmallInteger, nullable=True)
    max_players_recommended = Column(SmallInteger, nullable=True)
    play_time_min = Column(SmallInteger, nullable=True)
    play_time_max = Column(SmallInteger, nullable=True)
    tesera_url = Column(String(), nullable=True)
