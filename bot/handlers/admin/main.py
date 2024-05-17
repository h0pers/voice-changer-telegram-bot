from aiogram import Router, F

from bot.filters.is_admin import OnlyAdmin, OnlyAdminCallback
from bot.filters.not_banned import NotBannedUser, NotBannedUserCallback

from .admin_panel import admin_panel_router
from .callback.main import get_admin_callback_router

admin_router = Router()

admin_router.message.filter(OnlyAdmin())
admin_router.message.filter(NotBannedUser())
admin_router.message.filter(F.chat.type == 'private')
admin_router.callback_query.filter(OnlyAdminCallback())
admin_router.callback_query.filter(NotBannedUserCallback())
admin_router.callback_query.filter(F.chat.type == 'private')


def get_admin_router() -> Router:
    admin_routers = (admin_panel_router, get_admin_callback_router(),)
    admin_router.include_routers(*admin_routers)
    return admin_router
