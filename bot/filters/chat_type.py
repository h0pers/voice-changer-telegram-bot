from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class ChatType(BaseFilter):
    chat_types = []
    chats_id = []

    def __init__(self, chat_types: List[str], chats_id: List[str] = None):
        self.set_groups_ids(chats_id)
        self.chat_types = chat_types

    async def __call__(self, message: Message, *args,
                       **kwargs):
        self.chats_id.append(str(message.chat.id))
        if message.chat.type not in self.chat_types:
            return False

        return str(message.chat.id) in self.chats_id

    def set_groups_ids(self, groups_ids: List[str]):
        if groups_ids is not None:
            self.chats_id = groups_ids


class ChatTypeCallback(BaseFilter):
    chat_types = []
    chats_id = []

    def __init__(self, chat_types: List[str], chats_id: List[str] = None):
        self.set_groups_ids(chats_id)
        self.chat_types = chat_types

    async def __call__(self, query: CallbackQuery, *args,
                       **kwargs):
        self.chats_id.append(str(query.chat.id))
        if query.chat.type not in self.chat_types:
            return False

        return str(query.chat.id) in self.chats_id

    def set_groups_ids(self, groups_ids: List[str]):
        if groups_ids is not None:
            self.chats_id = groups_ids
