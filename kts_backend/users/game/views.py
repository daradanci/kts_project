import json

from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPUnauthorized,
    HTTPForbidden,
    HTTPConflict,
    HTTPBadRequest,
)
from aiohttp_apispec import response_schema, docs, request_schema
from sqlalchemy.orm import class_mapper

from kts_backend.users.game.models import *
from kts_backend.users.game.schemes import *
from kts_backend.web.app import View
from kts_backend.web.schemes import OkResponseSchema
from kts_backend.web.utils import json_response
from kts_backend.web.mixins import AuthRequiredMixin


class GetGameInfoView(AuthRequiredMixin, View):
    @docs(
        tags=["web"],
        summary="Game info",
        description="Get last game info with chat_id",
    )
    @response_schema(OkResponseSchema)
    async def get(self):
        game_info = await self.store.game.get_last_game(
            self.request.rel_url.query["chat_id"]
        )
        print(game_info)
        return json_response(
            data={
                "id": game_info.id,
                "chat_id": game_info.chat_id,
                "created_at": str(game_info.created_at),
                "players": [
                    {
                        "tg_id": player.tg_id,
                        "name": player.name,
                        "last_name": player.last_name,
                        "score": [score.points for score in player.score],
                    }
                    for player in game_info.players
                ],
            }
        )


class GetChatInfoView(AuthRequiredMixin, View):
    @docs(
        tags=["web"],
        summary="Get chat info",
        description="Get chat info using chat_id and tg_id",
    )
    @response_schema(OkResponseSchema)
    async def get(self):
        chat_info = await self.store.game.get_chat_info(
            chat_id=self.request.rel_url.query["chat_id"],
            tg_id=self.request.rel_url.query["user_id"]
            if "user_id" in self.request.rel_url.query
            else None,
        )
        return json_response(chat_info["result"])


class StartGameView(AuthRequiredMixin, View):
    @docs(
        tags=["web"],
        summary="Start game",
        description="Start new game with chat_id",
    )
    @request_schema(GameSchema)
    @response_schema(OkResponseSchema)
    async def post(self):
        new_game = await self.store.game.start_game(
            chat_id=self.data["chat_id"], players=self.data["players"]
        )

        return json_response(
            data={
                "id": new_game.id,
                "chat_id": new_game.chat_id,
                "created_at": str(new_game.created_at),
                "players": [
                    {
                        "tg_id": player.tg_id,
                        "name": player.name,
                        "last_name": player.last_name,
                        "score": [score.points for score in player.score],
                    }
                    for player in new_game.players
                ],
            }
        )
