from aiogram.types import KeyboardButton

from bot.keyboards.reply.main import Reply


class ChooseVoiceTypeReplyButtonText:
    TEXT_TYPE = 'Текст'
    VOICE_TYPE = 'Голосовое'
    BACK = '↩️ Назад'


text_type_button = KeyboardButton(text=ChooseVoiceTypeReplyButtonText.TEXT_TYPE)

voice_type_button = KeyboardButton(text=ChooseVoiceTypeReplyButtonText.VOICE_TYPE)

back_button = KeyboardButton(text=ChooseVoiceTypeReplyButtonText.BACK)


choose_voice_type_reply_markup = Reply([
    [text_type_button, voice_type_button, back_button],
])
