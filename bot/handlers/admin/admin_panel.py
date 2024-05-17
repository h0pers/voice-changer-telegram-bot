from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from bot.config import MessageText
from bot.fsm.user import UserState
from bot.keyboards.reply.admin.panel import admin_panel_reply_markup, AdminPanelTypeReplyButtonText
from bot.misc.util import get_voice_api_characters, start_newsletter, change_voice_api, change_voice_reply_chat_id, \
    change_voice_id

admin_panel_router = Router()


@admin_panel_router.message(Command(commands=['adminka']))
async def admin_panel_handler(message: Message):
    await message.answer(text=MessageText.ADMIN_PANEL_WELCOME, reply_markup=admin_panel_reply_markup.get_markup())


@admin_panel_router.message(StateFilter(None), F.text == AdminPanelTypeReplyButtonText.VOICE_API_CHARACTERS_LEFT)
async def get_voice_api_characters_handler(message: Message):
    voice_api_characters_data = await get_voice_api_characters()
    await message.answer(text=MessageText.VOICE_API_CHARACTERS_LEFT.format(
        characters_limit=voice_api_characters_data.get('characters_limit'),
        characters_count=voice_api_characters_data.get('characters_count'),
        characters_left=voice_api_characters_data.get('characters_left'),
    ))


@admin_panel_router.message(StateFilter(None), F.text == AdminPanelTypeReplyButtonText.CHANGE_VOICE_API_KEY)
async def setup_voice_api_handler(message: Message, state: FSMContext):
    await message.answer(text=MessageText.SETUP_VOICE_API)
    await state.set_state(UserState.SETUP_VOICE_API)


@admin_panel_router.message(StateFilter(UserState.SETUP_VOICE_API), F.text)
async def change_voice_api_handler(message: Message, state: FSMContext):
    await change_voice_api(message.text)
    await state.clear()


@admin_panel_router.message(StateFilter(None), F.text == AdminPanelTypeReplyButtonText.CHANGE_VOICE_ID)
async def setup_voice_id_handler(message: Message, state: FSMContext):
    await message.answer(text=MessageText.SETUP_VOICE_ID)
    await state.set_state(UserState.SETUP_VOICE_ID)


@admin_panel_router.message(StateFilter(UserState.SETUP_VOICE_ID), F.text)
async def change_voice_id_handler(message: Message, state: FSMContext):
    await change_voice_id(message.text)
    await state.clear()


@admin_panel_router.message(StateFilter(None), F.text == AdminPanelTypeReplyButtonText.CHANGED_VOICE_REPLY_CHAT)
async def setup_voice_reply_chat_handler(message: Message, state: FSMContext):
    await message.answer(text=MessageText.SETUP_VOICE_REPLY_ID)
    await state.set_state(UserState.SETUP_VOICE_REPLY_CHAT)


@admin_panel_router.message(StateFilter(UserState.SETUP_VOICE_REPLY_CHAT), F.text.regexp('^-?\d*\.{0,1}\d+$'))
async def change_voice_reply_chat_handler(message: Message, state: FSMContext):
    await change_voice_reply_chat_id(int(message.text))
    await state.clear()


@admin_panel_router.message(StateFilter(None), F.text == AdminPanelTypeReplyButtonText.NEWSLETTER)
async def setup_newsletter_handler(message: Message, state: FSMContext):
    await message.answer(text=MessageText.SETUP_NEWSLETTER)
    await state.set_state(UserState.SETUP_NEWSLETTER)


@admin_panel_router.message(StateFilter(UserState.SETUP_NEWSLETTER))
async def start_newsletter_handler(message: Message, bot: Bot, state: FSMContext):
    newsletter_stats = await start_newsletter(message, bot)
    await message.answer(text=MessageText.NEWSLETTER_START)
    await message.answer(text=MessageText.NEWSLETTER_FINISH.format(
        successful_executed=newsletter_stats.get('successful_executed'),
        unsuccessful_executed=newsletter_stats.get('unsuccessful_executed'),
        finish_time=newsletter_stats.get('finish_time'),
        users_amount=newsletter_stats.get('amount'),
    ))
    await state.clear()
