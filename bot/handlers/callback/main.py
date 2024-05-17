from aiogram import Router, F

from bot.filters.not_banned import NotBannedUserCallback

from .start import start_callback_router


other_callback_router = Router()

other_callback_router.callback_query.filter(NotBannedUserCallback())
other_callback_router.callback_query.filter(F.chat.type == 'private')


def get_other_callback_router() -> Router:
    other_callback_routers = (start_callback_router,)
    other_callback_router.include_routers(*other_callback_routers)

    return other_callback_router
