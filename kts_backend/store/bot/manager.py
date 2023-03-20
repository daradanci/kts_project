import typing
from logging import getLogger

from kts_backend.store.tg_api.dataclasses import Message, Update

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            await self.app.store.tg_api.send_message(
                Message(
                    chat_id=update.object.chat_id,
                    text=update.object.body,
                )
            )
