from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText
from bot.filters.not_banned import NotBannedUser, NotBannedUserCallback

cancel_router = Router()

cancel_router.message.filter(NotBannedUser())
cancel_router.message.filter(F.chat.type == 'private')
cancel_router.callback_query.filter(F.chat.type == 'private')
cancel_router.callback_query.filter(NotBannedUserCallback())


@cancel_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer(text=MessageText.CANCEL_SUCCESSFUL)
    await state.clear()
