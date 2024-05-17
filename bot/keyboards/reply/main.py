from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Reply:
    reply_buttons: List[List[KeyboardButton]]
    markup: ReplyKeyboardMarkup

    def __init__(self, buttons_list: List[List[KeyboardButton]]):
        self.reply_buttons = buttons_list

    def get_markup(self, **kwargs) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard=self.reply_buttons, resize_keyboard=True, is_persistent=True, **kwargs)


class ReplyButtonText:
    pass
