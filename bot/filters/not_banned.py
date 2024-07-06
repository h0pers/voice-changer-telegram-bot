import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.config import TIMEZONE
from bot.database.models.user import User, UserController


class NotBannedUser(BaseFilter):
    async def __call__(self, message: Message, user: User):
        if user.block_end_time is not None and user.block_end_time <= datetime.datetime.now(TIMEZONE):
            await UserController.unban(telegram_id=user.telegram_id)
            return True

        if user.is_blocked:
            return False

        return True


class NotBannedUserCallback(BaseFilter):
    async def __call__(self, query: CallbackQuery, user: User):
        if user.block_end_time is not None and user.block_end_time <= datetime.datetime.now(TIMEZONE):
            await UserController.unban(telegram_id=user.telegram_id)
            return True

        if user.is_blocked:
            return False

        return True
