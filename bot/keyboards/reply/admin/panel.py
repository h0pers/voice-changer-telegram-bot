from aiogram.types import KeyboardButton

from bot.keyboards.reply.main import Reply


class AdminPanelTypeReplyButtonText:
    CHANGE_VOICE_API_KEY = 'VOICE API ⚒️'
    VOICE_API_CHARACTERS_LEFT = 'API Статистика 📊'
    GLOBAL_STATISTIC = 'Статистика 📊'
    CHANGE_VOICE_ID = 'VOICE ID ⚒️'
    NEWSLETTER = 'Рассылка пользователям 🗞️'
    GIVE_VOICE_PREMIUM = 'Выдать VOICE Premium ✍️'
    REMOVE_VOICE_PREMIUM = 'Забрать VOICE Premium 🧹'
    CHANGED_VOICE_REPLY_CHAT = 'Группа обработанных голосовых 💬'
    CHANGE_VOICE_LIMIT = 'Изменить лимит на голосовые 🎤'
    CHANGE_TEXT_LIMIT = 'Изменить лимит на текстовые 📤'


change_voice_api_key = KeyboardButton(text=AdminPanelTypeReplyButtonText.CHANGE_VOICE_API_KEY)

change_voice_id = KeyboardButton(text=AdminPanelTypeReplyButtonText.CHANGE_VOICE_ID)

voice_id_characters_left = KeyboardButton(text=AdminPanelTypeReplyButtonText.VOICE_API_CHARACTERS_LEFT)

newsletter = KeyboardButton(text=AdminPanelTypeReplyButtonText.NEWSLETTER)

change_voice_reply_chat = KeyboardButton(text=AdminPanelTypeReplyButtonText.CHANGED_VOICE_REPLY_CHAT)

statistic = KeyboardButton(text=AdminPanelTypeReplyButtonText.GLOBAL_STATISTIC)

give_voice_premium = KeyboardButton(text=AdminPanelTypeReplyButtonText.GIVE_VOICE_PREMIUM)

remove_voice_premium = KeyboardButton(text=AdminPanelTypeReplyButtonText.REMOVE_VOICE_PREMIUM)

chnage_voice_limit = KeyboardButton(text=AdminPanelTypeReplyButtonText.CHANGE_VOICE_LIMIT)

chnage_text_limit = KeyboardButton(text=AdminPanelTypeReplyButtonText.CHANGE_TEXT_LIMIT)

admin_panel_reply_markup = Reply([
    [change_voice_api_key, change_voice_id],
    [newsletter, change_voice_reply_chat],
    [give_voice_premium, remove_voice_premium],
    [chnage_voice_limit, chnage_text_limit],
    [statistic, voice_id_characters_left],
])
