import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload, contains_eager

from kts_backend.users.game.models import GameDC, GameScoreDC, PlayerDC, GameModel, GameScoreModel, PlayerModel
from kts_backend.store import Store
from tests.game import game2dict, score2dict, player2dict
from tests.utils import check_empty_table_exists
from tests.utils import ok_response


class TestGame:
    @pytest.mark.asyncio
    async def test_tables_exist(self, cli):

        await check_empty_table_exists(cli, "games")
        await check_empty_table_exists(cli, "gamescores")
        await check_empty_table_exists(cli, "players")

    @pytest.mark.asyncio
    async def test_create_game(self, cli, store: Store, game_1: GameDC, players: list[PlayerDC]):
        game=await store.game.start_game(chat_id=game_1.chat_id, players=[player2dict(player) for player in players])
        assert type(game) is GameDC
        async with cli.app.database.session() as session:
            res = await session.execute(select(GameModel).filter_by(id=game_1.id))
            games = res.scalars().all()

        assert len(games) == 1
        db_game=games[0]
        assert db_game.chat_id==game_1.chat_id
        assert db_game.created_at==game_1.created_at

        game_info=await store.game.get_last_game(db_game.chat_id)
        assert len(game_info.players)==4

        for have, expected in zip(game_info.players,players):
            assert have.tg_id == expected.tg_id
            assert have.name == expected.name
            assert have.last_name == expected.last_name
            for have_points,expected_points in zip( expected.score,have.score):
                assert have_points.points == expected_points.points

    # @pytest.mark.asyncio
    # async def test_create_game_no_chat_id(self, cli, store: Store, game_1: GameDC, players: list[PlayerDC]):
    #     with pytest.raises(IntegrityError) as exc_info:
    #         await store.game.start_game(chat_id="", players=[player2dict(player) for player in players])
    #     assert exc_info.value.orig.pgcode == "23503"

    @pytest.mark.asyncio
    async def test_create_game_unique_players(self, cli, store: Store, game_1: GameDC, players: list[PlayerDC]):
        with pytest.raises(IntegrityError) as exc_info:
            await store.game.start_game(chat_id=game_1.chat_id,
                                               players=[player2dict(player) for player in players]
                                        +
                                                       [player2dict(player) for player in players]
                                        )
        assert exc_info.value.orig.pgcode == "23505"












        



