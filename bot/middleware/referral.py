from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

from bot.database.main import SessionLocal
from bot.database.models.main import User


class ReferralSystemMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == event.from_user.id)
            statement = await session.execute(query)
            try:
                statement.scalar_one()
                data.update({'is_new_user': False})
            except NoResultFound:
                data.update({'is_new_user': True})

        result = await handler(event, data)
        return result
