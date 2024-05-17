from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from mutagen.oggopus import OggOpus

from bot.config import MessageText
from bot.fsm.user import UserState
from bot.handlers.user.start import start_handler
from bot.keyboards.reply.choose_voice_type import choose_voice_type_reply_markup, ChooseVoiceTypeReplyButtonText
from bot.keyboards.reply.welcome import WelcomeReplyButtonText, welcome_reply_markup
from bot.misc.util import get_reply_chat_id, convert_text_to_speech, convert_speech_to_speech, get_telegram_users, \
    send_voice_reply, add_audio_processed_count

voice_router = Router()


@voice_router.message(StateFilter(UserState.PROCESSING_VOICE, UserState.PICKED_WOMAN_VOICE),
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
async def processing_voice_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    if data['voice_type'] == ChooseVoiceTypeReplyButtonText.TEXT_TYPE and message.text:
        voice = bytes()
        voice_data = await convert_text_to_speech(message.text)
        async for voice_part in voice_data:
            voice += voice_part

        voice_file = BufferedInputFile(voice, 'voice-result')
        await message.answer_voice(voice=voice_file, reply_markup=welcome_reply_markup.get_markup())
        await state.clear()
        await send_voice_reply(chat_id=await get_reply_chat_id(),
                               voice_file=voice_file,
                               message=message,
                               bot=bot)
        return

    if data['voice_type'] == ChooseVoiceTypeReplyButtonText.VOICE_TYPE and message.voice:
        admins_ids = await get_telegram_users(is_admin=True, is_blocked=False)
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        voice_bytes = await bot.download_file(file_path)
        voice_validator = OggOpus(voice_bytes)
        if voice_validator.info.length > 60:
            await message.answer(text=MessageText.VOICE_LENGTH_ERROR)
            return

        voice = BufferedInputFile(voice_bytes.read(), 'voice')
        for admin_id in admins_ids:
            await send_voice_reply(chat_id=admin_id,
                                   voice_file=voice,
                                   message=message,
                                   bot=bot)
        processed_voice = await convert_speech_to_speech(voice_bytes)
        processed_voice_file = BufferedInputFile(processed_voice, 'voice')

        await send_voice_reply(chat_id=await get_reply_chat_id(),
                               voice_file=processed_voice_file,
                               message=message,
                               bot=bot)
        await add_audio_processed_count(message.from_user.id)
        await message.answer_voice(voice=processed_voice_file, reply_markup=welcome_reply_markup.get_markup())
        await state.clear()
        return

    await message.answer('ERORRO', welcome_reply_markup.get_markup())
