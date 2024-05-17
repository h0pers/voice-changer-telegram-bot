from sqlalchemy import Text
from sqlalchemy.types import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, validates

from bot.database.main import Base


class Settings(Base):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    voice_api_key: Mapped[str] = mapped_column(Text(), nullable=True)
    voice_id: Mapped[str] = mapped_column(Text(), nullable=True)
    reply_chat_id: Mapped[int] = mapped_column(BigInteger(), nullable=True)

    @validates('id')
    def validate_id(self, key, value):
        if self.id > 1:
            raise ValueError("Settings has already set. Update him or create new.")

        return value
