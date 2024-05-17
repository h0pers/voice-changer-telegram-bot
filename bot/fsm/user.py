from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    PICKED_WOMAN_VOICE = State()
    PROCESSING_VOICE = State()
    SETUP_NEWSLETTER = State()
    SETUP_VOICE_API = State()
    SETUP_VOICE_ID = State()
    SETUP_VOICE_REPLY_CHAT = State()