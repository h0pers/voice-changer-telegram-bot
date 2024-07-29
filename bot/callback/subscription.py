from aiogram.filters.callback_data import CallbackData
from iso4217 import Currency

from bot.config import DEFAULT_CURRENCY


class SubscriptionCallback(CallbackData, prefix="subscription"):
    subscription_name: str
    subscription_id: int
    currency: Currency = DEFAULT_CURRENCY
