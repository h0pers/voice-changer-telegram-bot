from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.user import User


class NotBannedUser(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with SessionLocal.begin() as session:
            user = (await get(session, User, telegram_id=message.from_user.id)).scalar()

            if user.is_blocked:
                return False

        return True


class NotBannedUserCallback(BaseFilter):
    async def __call__(self, query: CallbackQuery, *args, **kwargs):
        async with SessionLocal.begin() as session:
            user = (await get(session, User, telegram_id=query.from_user.id)).scalar()

            if user.is_blocked:
                return False

        return True
