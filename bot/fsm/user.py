from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    PICKED_WOMAN_VOICE = State()
    PROCESSING_VOICE = State()