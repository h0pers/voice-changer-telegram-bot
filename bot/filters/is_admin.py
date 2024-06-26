from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.user import User


class OnlyAdmin(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with SessionLocal.begin() as session:
            print((await session.execute(select(User))).scalars().all())
            print((await get(session, User)).scalars().all())
            user = (await get(session, User, telegram_id=message.from_user.id)).scalar()

            if user.is_admin:
                return True

        return False


class OnlyAdminCallback(BaseFilter):
    async def __call__(self, query: CallbackQuery, *args, **kwargs):
        async with SessionLocal.begin() as session:
            print((await session.execute(select(User))).scalars())
            print((await get(session, User)).scalars())
            user = (await get(session, User, telegram_id=query.from_user.id)).scalar()

            if user.is_admin:
                return True

        return False
