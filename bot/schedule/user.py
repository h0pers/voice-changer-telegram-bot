from sqlalchemy import select

from bot.config import DAILY_AUDIO_ATTEMPT
from bot.database.main import SessionLocal
from bot.database.models.user import User


async def reset_audio_limits():
    async with SessionLocal.begin() as session:
        query = select(User)
        statement = await session.execute(query)
        users = statement.scalars().all()

        for user in users:
            user.audio_attempt_left = DAILY_AUDIO_ATTEMPT
