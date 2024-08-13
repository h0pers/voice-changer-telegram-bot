from abc import ABC, abstractmethod
from sqlalchemy import Text, select
from sqlalchemy.types import BigInteger, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, validates

from bot.database.main import Base, SessionLocal


class Settings(Base):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    voice_api_key: Mapped[str] = mapped_column(Text(), nullable=True)
    voice_id: Mapped[str] = mapped_column(Text(), nullable=True)
    reply_chat_id: Mapped[int] = mapped_column(BigInteger(), nullable=True)
    voice_seconds_limit: Mapped[int] = mapped_column(SmallInteger(), nullable=True)
    voice_text_characters_limit: Mapped[int] = mapped_column(SmallInteger(), nullable=True)

    @validates('id')
    def validate_id(self, key, value):
        if self.id > 1:
            raise ValueError("Settings has already set. Update him or create new.")

        return value


class VoiceTypeAbstract(ABC):
    @property
    @abstractmethod
    def voice_type(self) -> str:
        pass

    @abstractmethod
    async def set_voice_limit(self, limit: int):
        pass


class VoiceTypeLimit(VoiceTypeAbstract):
    voice_type = 'voice'

    async def set_voice_limit(self, limit: int):
        async with SessionLocal.begin() as session:
            query = select(Settings)
            statement = await session.execute(query)
            settings_model = statement.scalar_one()
            settings_model.voice_seconds_limit = limit


class TextTypeLimit(VoiceTypeAbstract):
    voice_type = 'text'

    async def set_voice_limit(self, limit: int):
        async with SessionLocal.begin() as session:
            query = select(Settings)
            statement = await session.execute(query)
            settings_model = statement.scalar_one()
            settings_model.voice_text_characters_limit = limit


class VoiceTypeFactory:
    voice_types = {
        'voice': VoiceTypeLimit,
        'text': TextTypeLimit,
    }

    def __call__(self, voice_type: str, *args, **kwargs) -> VoiceTypeAbstract:
        return self.get_voice_limit_manager(voice_type)

    @classmethod
    def get_voice_limit_manager(cls, voice_type: str) -> VoiceTypeAbstract:
        voice_type_class = cls.voice_types.get(voice_type)

        if not voice_type_class:
            raise KeyError(f'{voice_type} is not found in available types.')

        return voice_type_class()


class SettingsManager:
    @staticmethod
    async def get_settings_model() -> Settings:
        async with SessionLocal.begin() as session:
            query = select(Settings)
            statement = await session.execute(query)
            settings_model = statement.scalar_one()
            return settings_model

    @staticmethod
    async def set_voice_limit(voice_type: str, limit: int):
        voice_limit_manager = VoiceTypeFactory()(voice_type)
        await voice_limit_manager.set_voice_limit(limit)
