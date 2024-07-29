from aiogram import Router

from .start import start_router
from .callback.main import get_user_callback_router
from .voice import voice_router

user_router = Router()


def get_user_router() -> Router:
    user_routers = (start_router, voice_router,
                    get_user_callback_router(),)
    user_router.include_routers(*user_routers)

    return user_router
