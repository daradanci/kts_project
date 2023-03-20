from dataclasses import dataclass


@dataclass
class UpdateObject:
    # message_id: int
    chat_id: int
    user_id: int
    # username: str
    body: str


@dataclass
class Update:
    update_id: int
    object: UpdateObject


@dataclass
class Message:
    chat_id: int
    text: str