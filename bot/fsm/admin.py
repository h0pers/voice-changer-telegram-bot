from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    SETUP_NEWSLETTER = State()
    SETUP_VOICE_API = State()
    SETUP_VOICE_ID = State()
    SETUP_VOICE_REPLY_CHAT = State()
    GIVE_VOICE_PREMIUM = State()
    REMOVE_VOICE_PREMIUM = State()
