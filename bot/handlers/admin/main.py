from aiogram import Router

from bot.middleware.user import UserAdminCheckoutMiddleware
from .admin_panel import admin_panel_router
from .premium import premium_router
from .callback.main import get_admin_callback_router
from .ban import ban_router

admin_router = Router()

admin_router.message.middleware(UserAdminCheckoutMiddleware())
admin_router.callback_query.middleware(UserAdminCheckoutMiddleware())


def get_admin_router() -> Router:
    admin_routers = (admin_panel_router, ban_router, premium_router, get_admin_callback_router(),)
    admin_router.include_routers(*admin_routers)
    return admin_router
