import datetime

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, StateFilter, CommandObject
from sqlalchemy.exc import NoResultFound
from datetime import timedelta

from bot.config import MessageText, TIMEZONE
from bot.database.models.user import UserController

ban_router = Router()


@ban_router.message(StateFilter(None), Command('ban'))
async def ban_command_handler(message: Message, bot: Bot, command: CommandObject):
    try:
        command_args = command.args.split(' ')
    except AttributeError:
        await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
        return

    command_kwargs = {
        'telegram_id': command_args[0],
        'ban_days_amount': int(command_args[1]) if 1 < len(command_args) else None,
        'reason': ' '.join(command_args[2:]) if 2 < len(command_args) else None,
    }

    try:
        if not command_kwargs['ban_days_amount'].isnumeric():
            await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
            return

        if int(command_kwargs['ban_days_amount']) <= 0:
            await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
            return

    except AttributeError:
        pass

    try:
        block_end_time = datetime.datetime.now(TIMEZONE) + timedelta(days=command_kwargs['ban_days_amount'])
    except TypeError:
        block_end_time = None

    try:
        await UserController.ban(command_kwargs['telegram_id'], bot, block_end_time, command_kwargs['reason'])
        await message.answer(text=MessageText.BAN_SUCCESSFUL.format(telegram_id=command_kwargs['telegram_id']))
    except NoResultFound:
        await message.answer(text=MessageText.USER_IS_NOT_EXIST)
        return
    except ValueError:
        await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
        return


@ban_router.message(StateFilter(None), Command('unban'))
async def unban_command_handler(message: Message, command: CommandObject):
    try:
        command_args = command.args.split(' ')
    except AttributeError:
        await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
        return

    command_kwargs = {
        'telegram_id': command_args[0],
    }

    if not command_kwargs['telegram_id'].isnumeric():
        await message.answer(text=MessageText.COMMAND_SYNTAX_ERROR)
        return

    try:
        await UserController.unban(command_kwargs['telegram_id'])
        await message.answer(text=MessageText.UNBAN_SUCCESSFUL.format(telegram_id=command_kwargs['telegram_id']))
    except NoResultFound:
        await message.answer(text=MessageText.USER_IS_NOT_EXIST)
        return
