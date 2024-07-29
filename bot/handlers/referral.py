from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

from bot.database.models.user import UserController, User
from bot.handlers.user.start import start_handler

referral_router = Router()


@referral_router.message(CommandStart(deep_link=True))
async def referral_handler(message: Message, command: CommandObject, user: User, is_new_user: bool):
    referral_user = {
        "telegram_id": int(command.args)
    }
    if not is_new_user:
        return

    if referral_user['telegram_id'] == message.from_user.id:
        return

    await UserController.accept_referral(user.telegram_id, referral_user['telegram_id'])
    await start_handler(message)
