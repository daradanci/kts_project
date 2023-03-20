import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from kts_backend.users.game.models import (
GameDC, GameScoreDC, PlayerDC, GameModel, GameScoreModel, PlayerModel
)


@pytest.fixture
def players(store) -> list[PlayerDC]:
    return [
        PlayerDC(tg_id=7000, name='0', last_name='0', score=[GameScoreDC(points=0)]),
        PlayerDC(tg_id=7001, name='1', last_name='1', score=[GameScoreDC(points=0)]),
        PlayerDC(tg_id=7002, name='2', last_name='2', score=[GameScoreDC(points=0)]),
        PlayerDC(tg_id=7003, name='3', last_name='3', score=[GameScoreDC(points=0)]),
    ]



@pytest.fixture
async def player_1(db_session: AsyncSession) -> PlayerDC:
    name='Olivia'
    last_name='Milverton'
    tg_id=9000
    new_player=PlayerModel(tg_id=tg_id, name=name, last_name=last_name)
    async with db_session.begin() as session:
        session.add(new_player)
    return PlayerDC(tg_id=new_player.tg_id, name=new_player.name, last_name=new_player.last_name, score=[GameScoreDC(points=0)])



@pytest.fixture
async def player_2(db_session: AsyncSession) -> PlayerDC:
    name='Looney'
    last_name='Lovegood'
    tg_id=9001
    new_player=PlayerModel(tg_id=tg_id, name=name, last_name=last_name)
    async with db_session.begin() as session:
        session.add(new_player)
    return PlayerDC(tg_id=new_player.tg_id, name=new_player.name, last_name=new_player.last_name, score=[GameScoreDC(points=0)])

@pytest.fixture
async def game_1(db_session: AsyncSession) -> GameDC:
    chat_id=8000
    created_at=datetime.datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    new_game=GameModel(chat_id=chat_id,created_at=created_at)
    async with db_session.begin() as session:
        session.add(new_game)
    return GameDC(chat_id=new_game.chat_id,created_at=new_game.created_at, players=[], id=new_game.id)


@pytest.fixture
async def game_2(db_session: AsyncSession) -> GameDC:
    chat_id=8001
    created_at=datetime.datetime(year=2023, month=2, day=2, hour=0, minute=0, second=0, microsecond=0)
    new_game=GameModel(chat_id=chat_id,created_at=created_at)
    async with db_session.begin() as session:
        session.add(new_game)
    return GameDC(chat_id=new_game.chat_id,created_at=new_game.created_at, players=[], id=new_game.id)

@pytest.fixture
async def score_1(db_session: AsyncSession) -> GameScoreDC:

    new_score=GameScoreModel(points=0,player_id=9001,game_id=8000)
    async with db_session.begin() as session:
        session.add(new_score)
    return GameScoreDC(points=0)





