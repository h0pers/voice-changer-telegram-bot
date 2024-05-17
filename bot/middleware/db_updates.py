from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.database.main import SessionLocal
from bot.database.methods.update import update_or_create
from bot.database.models.main import User
from bot.database.methods.get import get


async def get_additional_data(message: Message) -> dict:
    async with SessionLocal.begin() as session:
        user = (await get(session, User, telegram_id=message.from_user.id)).scalar()
    return {
        'user': user,
    }


async def get_additional_callback_data(query: CallbackQuery) -> dict:
    async with SessionLocal.begin() as session:
        user = (await get(session, User, telegram_id=query.from_user.id)).scalar()

    return {
        'user': user,
    }


async def collect_user_data(message: Message) -> None:
    async with SessionLocal.begin() as session:
        await update_or_create(session=session,
                               instance=User,
                               values={
                                   'telegram_id': message.from_user.id,
                                   'username': message.from_user.username,
                                   'first_name': message.from_user.first_name,
                                   'last_name': message.from_user.last_name,
                                   'is_premium': message.from_user.is_premium or False,
                                   'language_code': message.from_user.language_code,
                               },
                               telegram_id=message.from_user.id
                               )
        print((await get(session, User)).scalars().all())
        print('asdasd')
        await session.commit()


async def collect_user_callback_data(query: CallbackQuery) -> None:
    async with SessionLocal.begin() as session:
        await update_or_create(session=session,
                               instance=User,
                               values={
                                   'telegram_id': query.from_user.id,
                                   'username': query.from_user.username,
                                   'first_name': query.from_user.first_name,
                                   'last_name': query.from_user.last_name,
                                   'is_premium': query.from_user.is_premium or False,
                                   'language_code': query.from_user.language_code,
                               },
                               telegram_id=query.from_user.id
                               )
        await session.commit()


class CollectData(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        await collect_user_data(event)
        data.update(await get_additional_data(event))
        result = await handler(event, data)
        return result


class CollectCallbackData(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        await collect_user_callback_data(event)
        data.update(await get_additional_callback_data(event))
        result = await handler(event, data)
        return result