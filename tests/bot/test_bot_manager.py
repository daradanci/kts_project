import pytest

from kts_backend.store.tg_api.dataclasses import Message, Update, UpdateObject


class TestHandleUpdates:
    @pytest.mark.asyncio
    async def test_no_messages(self, store):
        await store.bots_manager.handle_updates(updates=[])
        assert store.tg_api.send_message.called is False

    @pytest.mark.asyncio
    async def test_new_message(self, store):
        await store.bots_manager.handle_updates(
            updates=[
                Update(
                    update_id=1,
                    object=UpdateObject(
                        chat_id=1,
                        user_id=1,
                        body="Hello world!",
                    ),
                )
            ]
        )
        assert store.tg_api.send_message.call_count == 1
        message: Message = store.tg_api.send_message.mock_calls[0].args[0]
        assert message.chat_id == 1
        assert message.text
