from dataclasses import dataclass
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from kts_backend.store.database.sqlalchemy_base import db
from typing import Optional
import datetime


@dataclass
class GameDC:
    id: Optional[int]
    created_at: datetime
    chat_id: int
    players: Optional[list["PlayerDC"]]


@dataclass
class PlayerDC:
    tg_id: int
    name: str
    last_name: str
    score: Optional[list["GameScoreDC"]]


@dataclass
class GameScoreDC:
    points: Optional[int]
    # game: Optional['GameDC']
    # player: Optional['PlayerDC']


class GameModel(db):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    chat_id = Column(Integer, nullable=False)
    players = relationship("GameScoreModel", backref="games")


class PlayerModel(db):
    __tablename__ = "players"
    tg_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    score = relationship("GameScoreModel", backref="players")


class GameScoreModel(db):
    __tablename__ = "gamescores"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    points = Column(Integer, default=0)
    player_id = Column(
        Integer, ForeignKey("players.tg_id", ondelete="CASCADE"), nullable=False
    )
    game_id = Column(
        Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("player_id", "game_id", name="_player_in_game_score"),
    )
