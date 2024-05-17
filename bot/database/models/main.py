from bot.database.main import engine, Base, SessionLocal
from bot.database.methods.create import create
from .user import User
from .config import Settings


async def register_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with SessionLocal.begin() as session:
            await create(session, Settings, values={})
