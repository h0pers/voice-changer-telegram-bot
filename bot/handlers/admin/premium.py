from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, StateFilter, CommandObject
from datetime import datetime, timedelta

from bot.config import MessageText, TIMEZONE
from bot.database.models.user import UserController

premium_router = Router()


@premium_router.message(StateFilter(None), Command('premium'))
async def premium_command_handler(message: Message, bot: Bot, command: CommandObject):
    try:
        command_args = command.args.split(' ')
        if len(command_args) < 2:
            raise AttributeError()
    except AttributeError:
        await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
        return

    try:
        premium_days_amount = int(command_args[0].replace('d', ''))
        if premium_days_amount <= 0:
            raise ValueError()

    except ValueError:
        await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
        return

    command_kwargs = {
        'premium_days_amount': premium_days_amount,
        'telegram_id': int(command_args[1]) if command_args[1].isnumeric() else None,
    }

    if command_kwargs['telegram_id'] is None:
        await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
        return

    await UserController.give_voice_premium(telegram_id=command_kwargs['telegram_id'],
                                            premium_end_time=datetime.now(tz=TIMEZONE) + timedelta(days=command_kwargs['premium_days_amount']))
    await message.answer(text=MessageText.GIVE_VOICE_PREMIUM_SUCCESSFUL.format(telegram_id=command_kwargs['telegram_id']))


