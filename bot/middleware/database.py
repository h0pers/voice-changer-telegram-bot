from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from datetime import datetime

from bot.config import TIMEZONE
from bot.database.main import SessionLocal
from bot.database.methods.update import update_or_create
from bot.database.models.main import User, Settings
from bot.database.methods.get import get


class GatherInformationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with SessionLocal.begin() as session:
            await update_or_create(session=session,
                                   instance=User,
                                   values={
                                       'telegram_id': event.from_user.id,
                                       'username': event.from_user.username,
                                       'first_name': event.from_user.first_name,
                                       'last_name': event.from_user.last_name,
                                       'telegram_premium': event.from_user.is_premium or False,
                                       'language_code': event.from_user.language_code,
                                       'last_activity_date': datetime.now(tz=TIMEZONE),
                                   },
                                   telegram_id=event.from_user.id
                                   )
            await session.flush()
            user = (await get(session, User, telegram_id=event.from_user.id)).scalar()
            settings = (await get(session, Settings)).scalar()
            await session.commit()

        data.update({
            'user': user,
            'settings': settings,
        })
        result = await handler(event, data)
        return result
