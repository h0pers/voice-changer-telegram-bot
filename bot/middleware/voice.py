from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.config import MessageText, VOICE_CHARACTERS_MIN_REQUIRED
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

        if not user.audio_attempt_left + user.referral_audio_attempt_left and not user.is_audio_unlimited:
            await event.answer(text=MessageText.NO_VOICE_ATTEMPT)
            return

        result = await handler(event, data)
        return result
