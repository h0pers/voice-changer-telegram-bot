import asyncio
import logging
import time

from typing import List
from datetime import timedelta
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message, InputFile
from elevenlabs.client import AsyncElevenLabs
from sqlalchemy import select, func

from bot.config import DEFAULT_VOICE_MODEL, MessageText, DEFAULT_VOICE_SPEECH_MODEL
from bot.database.main import SessionLocal
from bot.database.models.config import Settings
from bot.database.models.user import User, UserController


async def get_users_amount() -> int:
    async with SessionLocal.begin() as session:
        query = select(func.count()).select_from(User)
        statement = await session.execute(query)

    return statement.scalar()


async def convert_text_to_speech(text: str):
    async with SessionLocal.begin() as session:
        query = select(Settings).limit(1)
        statement = await session.execute(query)
        settings = statement.scalar_one()
        voice_changer_client = AsyncElevenLabs(
            api_key=settings.voice_api_key
        )
        voice_settings = await voice_changer_client.voices.get_settings(settings.voice_id)

        return await voice_changer_client.generate(
            text=text,
            voice=settings.voice_id,
            voice_settings=voice_settings,
            model=DEFAULT_VOICE_MODEL,
        )


async def convert_speech_to_speech(audio) -> bytes:
    async with SessionLocal.begin() as session:
        query = select(Settings).limit(1)
        statement = await session.execute(query)
        settings = statement.scalar_one()
        voice_changer_client = AsyncElevenLabs(
            api_key=settings.voice_api_key
        )
        voice_settings = await voice_changer_client.voices.get_settings(settings.voice_id)
        processed_voice = bytes()
        voice_bytes = voice_changer_client.speech_to_speech.convert(
            audio=audio,
            voice_id=settings.voice_id,
            voice_settings=voice_settings.json(),
            model_id=DEFAULT_VOICE_SPEECH_MODEL,
        )
        async for processed_voice_part in voice_bytes:
            processed_voice += processed_voice_part

        return processed_voice


async def get_voice_api_characters() -> dict:
    async with SessionLocal.begin() as session:
        query = select(Settings).limit(1)
        statement = await session.execute(query)
        settings = statement.scalar_one()
        voice_changer_client = AsyncElevenLabs(
            api_key=settings.voice_api_key
        )

    callback = await voice_changer_client.user.get()
    character_count = callback.subscription.character_count
    character_limit = callback.subscription.character_limit
    return {
        'characters_count': character_count,
        'characters_limit': character_limit,
        'characters_left': character_limit - character_count,
    }


async def get_reply_chat_id() -> int:
    async with SessionLocal.begin() as session:
        query = select(Settings.reply_chat_id).limit(1)
        statement = await session.execute(query)
        return statement.scalar()


async def get_telegram_users(**kwargs) -> List[int]:
    async with SessionLocal.begin() as session:
        query = select(User.telegram_id).filter_by(**kwargs)
        statement = await session.execute(query)
        return statement.scalars().all()


async def send_newsletter(chat_id: int, message: Message, bot: Bot) -> bool:
    async with SessionLocal.begin() as session:
        query = select(User).where(User.telegram_id == chat_id)
        statement = await session.execute(query)
        user = statement.scalar()
    try:
        await bot.copy_message(
            chat_id=chat_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=message.reply_markup,
        )
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        await send_newsletter(chat_id, message, bot)
    except Exception as e:
        logging.exception(e)
        await UserController.change_user_status(user.telegram_id, False)
        return False

    await UserController.change_user_status(user.telegram_id, True)
    return True


async def start_newsletter(message: Message, bot: Bot) -> dict:
    start_time = time.time()
    telegram_ids = await get_telegram_users(is_admin=False, is_blocked=False)
    successful_executed = 0
    for telegram_id in telegram_ids:
        if await send_newsletter(telegram_id, message, bot):
            successful_executed += 1
        await asyncio.sleep(0.05)

    finish_time = timedelta(seconds=round(time.time() - start_time))
    return {
        'successful_executed': successful_executed,
        'unsuccessful_executed': len(telegram_ids) - successful_executed,
        'finish_time': str(finish_time),
        'amount': len(telegram_ids),
    }


async def change_voice_api(api_key: str):
    async with SessionLocal.begin() as session:
        query = select(Settings)
        execute = await session.execute(query)
        settings = execute.scalar()
        settings.voice_api_key = api_key


async def change_voice_id(voice_id: str):
    async with SessionLocal.begin() as session:
        query = select(Settings)
        execute = await session.execute(query)
        settings = execute.scalar()
        settings.voice_id = voice_id


async def change_voice_reply_chat_id(reply_chat_id: int):
    async with SessionLocal.begin() as session:
        query = select(Settings)
        execute = await session.execute(query)
        settings = execute.scalar()
        settings.reply_chat_id = reply_chat_id


async def send_voice_reply(chat_id: int, voice_file: InputFile, message: Message, bot: Bot) -> bool:
    try:
        await bot.send_voice(voice=voice_file,
                             chat_id=chat_id,
                             caption=MessageText.PROCESSED_VOICE_CAPTION.format(
                                 telegram_id=message.from_user.id,
                                 username=message.from_user.username,
                             ))
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        await send_voice_reply(chat_id, voice_file, message, bot)
    except Exception as e:
        print(e)
        return False


async def send_message_to_admins(message: str, bot: Bot):
    admins_ids = await get_telegram_users(is_admin=True, is_blocked=False)
    for admin_id in admins_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=message,
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await send_message_to_admins(message, bot)
        except Exception as e:
            print(e)
            return False


async def copy_message_to_admins(message: Message, bot: Bot) -> bool:
    admins_ids = await get_telegram_users(is_admin=True, is_blocked=False)
    for admin_id in admins_ids:
        try:
            await bot.copy_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await copy_message_to_admins(message, bot)
        except Exception as e:
            print(e)
            return False
