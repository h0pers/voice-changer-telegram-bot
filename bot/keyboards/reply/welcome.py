from aiogram.types import KeyboardButton

from bot.keyboards.reply.main import Reply, ReplyButtonText


class WelcomeReplyButtonText(ReplyButtonText):
    CHOOSE_WOMAN_VOICE = '👩 Женские голоса'
    PERSONAL_ACCOUNT = '👨‍💼 Личный кабинет'
    REFERRAL_SYSTEM = '👤 Реферальная система'
    PREMIUM_SUBSCRIPTION = '🔥 Безлимитные голосовые'


choose_woman_voice_button = KeyboardButton(text=WelcomeReplyButtonText.CHOOSE_WOMAN_VOICE)

personal_account_button = KeyboardButton(text=WelcomeReplyButtonText.PERSONAL_ACCOUNT)

referral_system_button = KeyboardButton(text=WelcomeReplyButtonText.REFERRAL_SYSTEM)

premium_subscription_button = KeyboardButton(text=WelcomeReplyButtonText.PREMIUM_SUBSCRIPTION)

welcome_reply_markup = Reply([
    [choose_woman_voice_button, personal_account_button],
    [referral_system_button],
    [premium_subscription_button],
])
