from aiogram.types import KeyboardButton

from bot.keyboards.reply.main import Reply


class WelcomeReplyButtonText:
    CHOOSE_WOMAN_VOICE = '👩 Женские голоса'
    PERSONAL_ACCOUNT = '👨‍💼 Личный кабинет'
    REFERRAL_SYSTEM = '👤 Реферальная система'


choose_woman_voice_button = KeyboardButton(text=WelcomeReplyButtonText.CHOOSE_WOMAN_VOICE)

personal_account_button = KeyboardButton(text=WelcomeReplyButtonText.PERSONAL_ACCOUNT)

referral_system_button = KeyboardButton(text=WelcomeReplyButtonText.REFERRAL_SYSTEM)

welcome_reply_markup = Reply([
    [choose_woman_voice_button, personal_account_button],
    [referral_system_button],
])
