import datetime
import os.path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from bot.handlers.main import get_all_routers
from bot.config import BOT_TOKEN, REDIS_PORT, REDIS_HOST, TIMEZONE, BASE_DIR
from bot.middleware.database import GatherInformationMiddleware
from bot.middleware.referral import ReferralSystemMiddleware
from bot.middleware.user import UserBanCheckoutMiddleware
from bot.middleware.voice import VoicePremiumMiddleware
from bot.schedule.user import reset_audio_limits

dp = Dispatcher(storage=RedisStorage(Redis(host=REDIS_HOST, port=REDIS_PORT)))

dp.message.filter(F.chat.type == 'private')
dp.message.outer_middleware(ReferralSystemMiddleware())
dp.message.outer_middleware(GatherInformationMiddleware())
dp.message.outer_middleware(UserBanCheckoutMiddleware())
dp.message.outer_middleware(VoicePremiumMiddleware())

dp.callback_query.filter(F.message.chat.type == 'private')
dp.callback_query.outer_middleware(ReferralSystemMiddleware())
dp.callback_query.outer_middleware(GatherInformationMiddleware())
dp.callback_query.outer_middleware(UserBanCheckoutMiddleware())
dp.callback_query.outer_middleware(VoicePremiumMiddleware())


async def start_bot():
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))
    scheduler = AsyncIOScheduler(timezone=TIMEZONE.zone)
    scheduler.add_job(reset_audio_limits, trigger='cron', hour=0, minute=0, start_date=datetime.datetime.now(TIMEZONE))
    scheduler.start()
    dp.include_routers(*get_all_routers())
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
