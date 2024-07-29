from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import MessageText

cancel_router = Router()


@cancel_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer(text=MessageText.CANCEL_SUCCESSFUL)
    await state.clear()
