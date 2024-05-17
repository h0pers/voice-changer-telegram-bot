from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from bot.database.models.main import register_models
from bot.handlers.main import get_all_routers

from bot.config import BOT_TOKEN, REDIS_PORT, REDIS_HOST
from bot.middleware.db_updates import CollectData, CollectCallbackData

dp = Dispatcher(storage=RedisStorage(Redis(host=REDIS_HOST, port=REDIS_PORT)))


async def start_bot():
    await register_models()
    dp.message.outer_middleware(CollectData())
    dp.message.outer_middleware(CollectCallbackData())
    dp.include_routers(*get_all_routers())
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
