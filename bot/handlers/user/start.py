from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callback.subscription import SubscriptionCallback
from bot.config import MessageText, REFERRAL_INCOME, STRFTIME_DEFAULT_FORMAT
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
        voice_attempt_left='безлимит' if user.is_audio_unlimited else user.audio_attempt_left + user.referral_audio_attempt_left
    ))


@start_router.message(StateFilter(None), F.text == WelcomeReplyButtonText.REFERRAL_SYSTEM)
async def account_referral_handler(message: Message):
    await message.answer(text=MessageText.REFERRAL_TEMPORARY_DISABLED)


@start_router.message(StateFilter(None), F.text == WelcomeReplyButtonText.PREMIUM_SUBSCRIPTION)
async def subscription_details_handler(message: Message, user: User):
    if user.is_audio_unlimited:
        await message.answer(text=MessageText.VOICE_PREMIUM_DETAILS.format(
            premium_end_time=user.audio_unlimited_end_time.strftime(STRFTIME_DEFAULT_FORMAT) if user.audio_unlimited_end_time else 'не установлено'))
        return

    builder = InlineKeyboardBuilder()
    builder.button(text='6.99$ / 7 дней',
                   callback_data=SubscriptionCallback(subscription_name='voice', subscription_id=1).pack())
    builder.button(text='12.99$ / 14 дней',
                   callback_data=SubscriptionCallback(subscription_name='voice', subscription_id=2).pack())
    builder.button(text='19.99$ / 30 дней',
                   callback_data=SubscriptionCallback(subscription_name='voice', subscription_id=3).pack())

    await message.answer(text=MessageText.BUY_PREMIUM_SUBSCRIPTION,
                         reply_markup=builder.as_markup(),
                         disable_web_page_preview=True)
