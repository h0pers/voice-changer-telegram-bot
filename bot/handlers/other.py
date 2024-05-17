from aiogram import Router, F

from bot.filters.not_banned import NotBannedUser, NotBannedUserCallback


other_router = Router()

other_router.message.filter(NotBannedUser())
other_router.message.filter(F.chat.type == 'private')
other_router.callback_query.filter(F.chat.type == 'private')
other_router.callback_query.filter(NotBannedUserCallback())
