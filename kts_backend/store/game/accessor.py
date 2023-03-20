import datetime
from typing import Optional
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict, HTTPBadRequest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload
from kts_backend.store.base.base_accessor import BaseAccessor
from kts_backend.users.game.models import (
    GameDC,
    GameScoreDC,
    PlayerDC,
    GameModel,
    GameScoreModel,
    PlayerModel,
)
from kts_backend.store.database.database import Database
from sqlalchemy import select, text, exc, delete

# from kts_backend.store.tg_api.accessor import TgApiAccessor


class GameAccessor(BaseAccessor):
    async def start_game(self, chat_id: int, players) -> Optional[GameDC]:
        async with self.app.database.session() as session:
            new_game = GameModel(chat_id=int(chat_id))
            session.add(new_game)
            await session.commit()
            print(players)
            new_players = []
            for player in players:
                new_player = await self.check_player(player)
                new_players.append(
                    PlayerDC(
                        tg_id=new_player.tg_id,
                        name=new_player.name,
                        last_name=new_player.last_name,
                        score=[await self.bind_player(new_game, new_player)],
                    )
                )

            return GameDC(
                id=new_game.id,
                chat_id=new_game.chat_id,
                players=new_players,
                created_at=new_game.created_at,
            )

    async def bind_player(self, new_game, new_player) -> Optional[GameScoreDC]:
        async with self.app.database.session() as session:
            new_gamescore = GameScoreModel(
                player_id=new_player.tg_id, game_id=new_game.id
            )
            session.add(new_gamescore)
            await session.commit()
            return GameScoreDC(points=new_gamescore.points)

    async def check_player(self, new_player) -> Optional[PlayerDC]:
        async with self.app.database.session() as session:
            result_raw = await session.execute(
                select(PlayerModel).filter_by(tg_id=new_player["tg_id"])
            )
            result = [res._mapping["PlayerModel"] for res in result_raw]
            return (
                result[0]
                if len(result) > 0
                else await self.add_player(new_player)
            )

    async def add_player(self, player) -> Optional[PlayerDC]:
        async with self.app.database.session() as session:
            new_player = PlayerModel(
                tg_id=player["tg_id"],
                name=player["name"],
                last_name=player["last_name"],
            )
            session.add(new_player)
            await session.commit()
            return PlayerDC(
                tg_id=new_player.tg_id,
                name=new_player.name,
                last_name=new_player.last_name,
                score=[],
            )

    async def get_last_game(self, chat_id: int) -> Optional[GameDC]:
        async with self.app.database.session() as session:
            result_raw = await session.execute(
                select(GameModel)
                .filter_by(chat_id=int(chat_id))
                .order_by("created_at")
            )
            result = [res._mapping["GameModel"] for res in result_raw]

            if len(result) > 0:
                last_game = result[-1]
            else:
                raise HTTPNotFound(
                    reason=f"There are no games in chat #{chat_id}"
                )
            self.logger.info(last_game)
            players_raw = await session.execute(
                select(GameModel, GameScoreModel, PlayerModel)
                .join(GameScoreModel, GameModel.id == GameScoreModel.game_id)
                .join(
                    PlayerModel, PlayerModel.tg_id == GameScoreModel.player_id
                )
                .where(GameModel.id == last_game.id)
            )
            players = [
                PlayerDC(
                    tg_id=player.tg_id,
                    name=player.name,
                    last_name=player.last_name,
                    score=[GameScoreDC(points=score.points)],
                )
                for (game, score, player) in players_raw
            ]

            return GameDC(
                id=int(last_game.id),
                created_at=last_game.created_at,
                chat_id=int(last_game.chat_id),
                players=players,
            )

    async def get_chat_info(self, chat_id: int, tg_id: int):
        return await self.app.store.tg_api.get_chat_info(
            chat_id=chat_id, tg_id=tg_id
        )
