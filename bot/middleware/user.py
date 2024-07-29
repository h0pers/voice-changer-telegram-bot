from datetime import datetime
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.config import TIMEZONE
from bot.database.main import SessionLocal
from bot.database.methods.get import get
from bot.database.models.user import UserController, User


class UserBanCheckoutMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        is_blocked = data['user'].is_blocked
        if data['user'].block_end_time is not None:
            if TIMEZONE.localize(data['user'].block_end_time) <= datetime.now(tz=TIMEZONE):
                await UserController.unban(telegram_id=data['user'].telegram_id)
                is_blocked = False

        if is_blocked:
            return

        result = await handler(event, data)
        return result


class UserAdminCheckoutMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        async with SessionLocal.begin() as session:
            user = (await get(session, User, telegram_id=event.from_user.id)).scalar()

            if not user.is_admin:
                return

        result = await handler(event, data)
        return result
