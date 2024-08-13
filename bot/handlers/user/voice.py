import io
import os.path
import uuid
import aiofiles

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from mutagen.oggopus import OggOpus
from pydub import AudioSegment

from bot.config import MessageText, BASE_DIR
from bot.database.models.user import UserController, User
from bot.database.models.config import Settings
from bot.fsm.user import UserState
from bot.handlers.user.start import start_handler
from bot.keyboards.reply.choose_voice_type import choose_voice_type_reply_markup, ChooseVoiceTypeReplyButtonText
from bot.keyboards.reply.welcome import WelcomeReplyButtonText, welcome_reply_markup
from bot.middleware.voice import VoiceUserPermissionMiddleware, VoiceClientMiddleware
from bot.misc.util import get_reply_chat_id, convert_text_to_speech, convert_speech_to_speech, copy_message_to_admins, \
    send_voice_reply, send_message_to_admins

voice_router = Router()
voice_return_router = Router()

voice_router.message.middleware(VoiceClientMiddleware())
voice_router.message.middleware(VoiceUserPermissionMiddleware())


@voice_return_router.message(StateFilter(UserState.PROCESSING_VOICE, UserState.PICKED_WOMAN_VOICE),
                             F.text == ChooseVoiceTypeReplyButtonText.BACK)
async def back_handler(message: Message, state: FSMContext):
    await start_handler(message)
    await state.clear()


@voice_router.message(StateFilter(None), F.text == WelcomeReplyButtonText.CHOOSE_WOMAN_VOICE)
async def picked_woman_voice_handler(message: Message, state: FSMContext):
    await message.answer_sticker('CAACAgIAAxkBAAJW4WZCFqRwVfCN5djVAqILAyo1SIc2AAIWAAMOR8coRysXvrD3mTQ1BA')
    await message.answer(text=MessageText.PICKED_WOMAN_VOICE_WELCOME,
                         reply_markup=choose_voice_type_reply_markup.get_markup())
    await state.set_state(UserState.PICKED_WOMAN_VOICE)
    await state.update_data({'voice_gender_type': message.text})


@voice_router.message(StateFilter(UserState.PICKED_WOMAN_VOICE),
                      F.text.in_({
                          ChooseVoiceTypeReplyButtonText.VOICE_TYPE,
                          ChooseVoiceTypeReplyButtonText.TEXT_TYPE,
                      }))
async def picked_woman_voice_type_handler(message: Message, state: FSMContext):
    if message.text == ChooseVoiceTypeReplyButtonText.TEXT_TYPE:
        await message.answer_sticker('CAACAgIAAxkBAAJX8GZH3q0AAbiFW3jptoTpxejoxcto2AACFQADDkfHKN9bk18wSjcfNQQ')
        await message.answer(text=MessageText.TEXT_CONVERTING_WELCOME)
    else:
        await message.answer_sticker('CAACAgIAAxkBAAJX82ZH3s9wiaBEZmtHv9IZnAABYVutNwACMwADDkfHKGxLD9RFtmVqNQQ')
        await message.answer(text=MessageText.SPEECH_CONVERTING_WELCOME)

    await state.update_data({'voice_type': message.text})
    await state.set_state(UserState.PROCESSING_VOICE)


@voice_router.message(StateFilter(UserState.PROCESSING_VOICE), or_f(F.text, F.voice))
async def processing_voice_handler(message: Message, bot: Bot, state: FSMContext, user: User, settings: Settings):
    data = await state.get_data()
    await UserController.subtract_voice_attempt(user.telegram_id)
    await UserController.add_audio_processed_count(user.telegram_id)

    if data['voice_type'] == ChooseVoiceTypeReplyButtonText.TEXT_TYPE and message.text:
        try:
            if len(message.text) > settings.voice_text_characters_limit and not user.is_audio_unlimited:
                await message.answer(text=MessageText.VOICE_LENGTH_ERROR)
                return
        except TypeError:
            pass

        voice = bytes()
        voice_data = await convert_text_to_speech(message.text)
        async for voice_part in voice_data:
            voice += voice_part

        voice_filename = f'{str(uuid.uuid4())}.mp3'
        voice_file_path = os.path.join(BASE_DIR, voice_filename)
        async with aiofiles.open(voice_file_path, mode='wb') as file:
            await file.write(voice)

        voice_converter = AudioSegment.from_mp3(voice_file_path)
        os.remove(voice_file_path)
        voice_converted = io.BytesIO()
        voice_converter.export(voice_converted, format='opus')
        voice_file = BufferedInputFile(voice_converted.read(), 'voice-result')
        await message.answer_voice(voice=voice_file, reply_markup=welcome_reply_markup.get_markup())
        await state.clear()
        await send_voice_reply(chat_id=await get_reply_chat_id(),
                               voice_file=voice_file,
                               message=message,
                               bot=bot)

        return

    if data['voice_type'] == ChooseVoiceTypeReplyButtonText.VOICE_TYPE and message.voice:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        voice_bytes = await bot.download_file(file_path)
        voice_validator = OggOpus(voice_bytes)
        try:
            if voice_validator.info.length > settings.voice_seconds_limit and not user.is_audio_unlimited:
                await message.answer(text=MessageText.VOICE_LENGTH_ERROR)
                return
        except TypeError:
            pass

        await copy_message_to_admins(message, bot)
        await send_message_to_admins(
            MessageText.PROCESSED_VOICE_CAPTION.format(
                telegram_id=message.from_user.id,
                username=message.from_user.username),
            bot
        )
        processed_voice = await convert_speech_to_speech(voice_bytes)
        voice_filename = f'{str(uuid.uuid4())}.mp3'
        voice_file_path = os.path.join(BASE_DIR, voice_filename)
        async with aiofiles.open(voice_file_path, mode='wb') as file:
            await file.write(processed_voice)

        voice_converter = AudioSegment.from_mp3(voice_file_path)
        os.remove(voice_file_path)
        voice_converted = io.BytesIO()
        voice_converter.export(voice_converted, format='opus')
        processed_voice_file = BufferedInputFile(voice_converted.read(), 'voice-result')

        await send_voice_reply(chat_id=await get_reply_chat_id(),
                               voice_file=processed_voice_file,
                               message=message,
                               bot=bot)
        await message.answer_voice(voice=processed_voice_file, reply_markup=welcome_reply_markup.get_markup())
        await state.clear()
        return
