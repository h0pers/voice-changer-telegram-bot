import logging
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy import select

from bot.config import MessageText, VOICE_CHARACTERS_MIN_REQUIRED, TIMEZONE
from bot.database.main import SessionLocal
from bot.database.models.user import UserController, User
from bot.misc.util import get_voice_api_characters, send_message_to_admins


class VoiceClientMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        response = await get_voice_api_characters()
        if response['characters_left'] <= VOICE_CHARACTERS_MIN_REQUIRED:
            await send_message_to_admins(MessageText.VOICE_CHARACTERS_LACK_ADMIN, data['bot'])
            await event.answer(text=MessageText.VOICE_CHARACTERS_LACK)
            return

        result = await handler(event, data)
        return result


class VoiceUserPermissionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user = data['user']

        if user.audio_attempt_left + user.referral_audio_attempt_left == 0 and user.is_audio_unlimited is False:
            await event.answer(text=MessageText.NO_VOICE_ATTEMPT)
            return

        result = await handler(event, data)
        return result


class VoicePremiumMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if data['user'].audio_unlimited_end_time is not None:
            if TIMEZONE.localize(data['user'].audio_unlimited_end_time) <= datetime.now(tz=TIMEZONE):
                await UserController.remove_voice_premium(event.from_user.id)
                async with SessionLocal.begin() as session:
                    query = select(User).where(User.telegram_id == event.from_user.id)
                    statement = await session.execute(query)
                    data['user'] = statement.scalar_one()

        result = await handler(event, data)
        return result
