from aiogram import Router

from .subscription import subscription_callback_router

user_callback_router = Router()


def get_user_callback_router() -> Router:
    user_callback_routers = (subscription_callback_router,)
    user_callback_router.include_routers(*user_callback_routers)

    return user_callback_router
