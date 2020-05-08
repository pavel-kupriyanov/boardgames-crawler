from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, SmallInteger, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)

many_to_many = Table('category_game_mtm', Base.metadata,
                     Column('game_category_id', Integer, ForeignKey('game_category.id')),
                     Column('game_id', Integer, ForeignKey('game.id'))
                     )


class Category(Base):
    __tablename__ = 'game_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    children = relationship("Game", secondary=many_to_many)


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    tesera_id = Column(Integer, unique=True)
    name = Column(String(250), unique=True)
    en_name = Column(String(250), unique=True)
    description = Column(String())
    photoUrl = Column(String(), nullable=True)
    bgg_rating = Column(Float)
    min_players = Column(SmallInteger, default=2)
    min_players_recommended = Column(SmallInteger, default=2)
    max_players = Column(SmallInteger)
    max_players_recommended = Column(SmallInteger)
    play_time_min = Column(SmallInteger)
    play_time_max = Column(SmallInteger)
    tesera_url = Column(String())
