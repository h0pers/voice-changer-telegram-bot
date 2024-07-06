import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.database.models.main import register_models
from bot.handlers.main import get_all_routers
from bot.config import BOT_TOKEN, REDIS_PORT, REDIS_HOST, TIMEZONE
from bot.middleware.db_updates import CollectData, CollectCallbackData
from bot.schedule.user import reset_audio_limits

dp = Dispatcher(storage=RedisStorage(Redis(host=REDIS_HOST, port=REDIS_PORT)))


async def start_bot():
    await register_models()
    scheduler = AsyncIOScheduler(timezone=TIMEZONE.zone)
    scheduler.add_job(reset_audio_limits, trigger='cron', hour=0, minute=0, start_date=datetime.datetime.now(TIMEZONE))
    scheduler.start()
    dp.message.outer_middleware(CollectData())
    dp.message.outer_middleware(CollectCallbackData())
    dp.include_routers(*get_all_routers())
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
