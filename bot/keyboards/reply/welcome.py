from aiogram.types import KeyboardButton

from bot.keyboards.reply.main import Reply


class WelcomeReplyButtonText:
    CHOOSE_WOMAN_VOICE = '👩 Женские голоса'
    PERSONAL_ACCOUNT = '👨‍💼 Личный кабинет'


choose_woman_voice_button = KeyboardButton(text=WelcomeReplyButtonText.CHOOSE_WOMAN_VOICE)

personal_account_button = KeyboardButton(text=WelcomeReplyButtonText.PERSONAL_ACCOUNT)

welcome_reply_markup = Reply([
    [choose_woman_voice_button],
    [personal_account_button]
])
