from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from sqlalchemy import func, select

from bot.config import MessageText
from bot.database.main import SessionLocal
from bot.database.models.user import User
from bot.keyboards.reply.welcome import welcome_reply_markup, WelcomeReplyButtonText

start_router = Router()


@start_router.message(StateFilter(None), CommandStart())
async def start_handler(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAJW22ZCFX4_m4ltpOpbqU6ir9_r4-3WAAILAAMOR8coqKD0-uKs4cE1BA')
    await message.answer(text=MessageText.WELCOME, reply_markup=welcome_reply_markup.get_markup())


@start_router.message(StateFilter(None), F.text == WelcomeReplyButtonText.PERSONAL_ACCOUNT)
async def account_stats_handler(message: Message, user: User):
    await message.answer_sticker('CAACAgIAAxkBAAJW3mZCFfzKVId4KU5uRnTmmH-PzrDSAAIPAAMOR8coKchfPDiosqM1BA')
    async with SessionLocal.begin() as session:
        query = select(func.count()).select_from(User)
        bot_users_amount = (await session.execute(query)).scalar()

        await message.answer(text=MessageText.USER_ACCOUNT_STATS.format(
            telegram_id=message.from_user.id,
            bot_users_amount=bot_users_amount,
            audio_processed_amount=user.audio_processed_count,
        ))
