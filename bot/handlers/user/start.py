from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from sqlalchemy import func, select

from bot.config import MessageText, REFERRAL_INCOME
from bot.database.main import SessionLocal
from bot.database.models.user import User, UserController
from bot.keyboards.reply.welcome import welcome_reply_markup, WelcomeReplyButtonText

start_router = Router()


@start_router.message(StateFilter(None), CommandStart())
async def start_handler(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAJW22ZCFX4_m4ltpOpbqU6ir9_r4-3WAAILAAMOR8coqKD0-uKs4cE1BA')
    await message.answer(text=MessageText.WELCOME, reply_markup=welcome_reply_markup.get_markup())


@start_router.message(StateFilter(None), F.text == WelcomeReplyButtonText.PERSONAL_ACCOUNT)
async def account_stats_handler(message: Message, user: User):
    await message.answer_sticker('CAACAgIAAxkBAAJW3mZCFfzKVId4KU5uRnTmmH-PzrDSAAIPAAMOR8coKchfPDiosqM1BA')
    await message.answer(text=MessageText.USER_ACCOUNT_STATS.format(
        telegram_id=message.from_user.id,
        audio_processed_amount=user.audio_processed_count,
        voice_attempt_left=user.audio_attempt_left + user.referral_audio_attempt_left
    ))


@start_router.message(StateFilter(None), F.text == WelcomeReplyButtonText.REFERRAL_SYSTEM)
async def account_referral_handler(message: Message, bot: Bot, user: User):

    await message.answer(text=MessageText.REFERRAL_ACCOUNT_INFO.format(
        referral_link=await UserController.create_referral(user, bot),
        total_referrals=user.referral_successful_count,
        referral_audio_attempt_left=user.referral_audio_attempt_left,
        referral_audio_attempt_total=user.referral_successful_count * REFERRAL_INCOME,
        referal_income=REFERRAL_INCOME,
    ))
