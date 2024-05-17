from aiogram import Router

from .start import start_callback_router

admin_callback_router = Router()


def get_admin_callback_router() -> Router:
    admin_callback_routers = (start_callback_router,)
    admin_callback_router.include_routers(*admin_callback_routers)

    return admin_callback_router
