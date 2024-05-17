from aiogram import Router, F

from bot.filters.not_banned import NotBannedUserCallback, NotBannedUser

from .start import start_router
from .callback.main import get_user_callback_router
from .voice import voice_router

user_router = Router()

user_router.message.filter(NotBannedUser())
user_router.message.filter(F.chat.type == 'private')
user_router.callback_query.filter(NotBannedUserCallback())
user_router.callback_query.filter(F.chat.type == 'private')


def get_user_router() -> Router:
    user_routers = (start_router, voice_router,
                    get_user_callback_router(),)
    user_router.include_routers(*user_routers)

    return user_router
