import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callback.subscription import SubscriptionCallback
from bot.config import MessageText

subscription_callback_router = Router()


@subscription_callback_router.callback_query(SubscriptionCallback.filter())
async def buy_subscription_handler(query: CallbackQuery, callback_data: SubscriptionCallback):
    await query.answer(text=MessageText.BUY_PREMIUM_SUBSCRIPTION_ANSWER)
