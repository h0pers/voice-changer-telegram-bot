import datetime

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from sqlalchemy import BigInteger, String, DateTime, Boolean, Integer, func, select, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from bot.config import REFERRAL_INCOME, MessageText, STRFTIME_DEFAULT_FORMAT, TIMEZONE
from bot.database.main import Base, SessionLocal


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger())
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    is_premium: Mapped[bool]
    language_code: Mapped[str] = mapped_column(String(35))
    registration_date: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())
    last_activity_date: Mapped[datetime.datetime] = mapped_column(DateTime(),
                                                                  server_default=func.now(),
                                                                  server_onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    audio_processed_count: Mapped[int] = mapped_column(Integer(), default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    block_end_time: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    is_audio_unlimited: Mapped[bool] = mapped_column(Boolean(), default=False)
    audio_attempt_left: Mapped[int] = mapped_column(Integer(), default=5)
    referral_audio_attempt_left: Mapped[int] = mapped_column(Integer(), default=0)
    referral_successful_count: Mapped[int] = mapped_column(Integer(), default=0)
    referral_friend_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    referral_friends = relationship("User", backref="referred_by", remote_side=[id])

    @validates('block_end_time')
    def validate_datetime_in_future(self, key, value: datetime.datetime):
        if value is None:
            return value

        if value <= datetime.datetime.now(TIMEZONE):
            raise ValueError('The date have to be in the future.')

        return value

    @validates('audio_attempt_left', 'audio_processed_count',
               'referral_audio_attempt_left', 'referral_successful_count')
    def validate_more_than_zero(self, key, value):
        if value < 0:
            raise ValueError('The value can not be lower than zero.')

        return value

    @hybrid_property
    def full_name(self):
        if self.last_name is None:
            return self.first_name

        return self.first_name + " " + self.last_name


class UserController:
    @classmethod
    async def give_voice_premium(cls, telegram_id: int):
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user = statement.scalar_one()
            user.is_audio_unlimited = True

    @classmethod
    async def remove_voice_premium(cls, telegram_id: int):
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user = statement.scalar_one()
            user.is_audio_unlimited = False

    @classmethod
    async def accept_referral(cls, telegram_id: int, referral_id: int):
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user_obj = statement.scalar_one()

            query = select(User).where(User.telegram_id == referral_id)
            statement = await session.execute(query)
            referral_owner = statement.scalar_one()

            user_obj.referral_friend_id = referral_owner.id
            referral_owner.referral_successful_count += 1
            referral_owner.referral_audio_attempt_left += REFERRAL_INCOME

    @classmethod
    async def create_referral(cls, user: User, bot: Bot) -> str:
        invite_link = await create_start_link(bot, user.telegram_id)
        return invite_link

    @classmethod
    async def add_audio_processed_count(cls, telegram_id: int):
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user_obj = statement.scalar_one()
            user_obj.audio_processed_count += 1

    @classmethod
    async def change_user_status(cls, telegram_id: int, status: bool):
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user_obj = statement.scalar_one()
            user_obj.is_active = status

    @classmethod
    async def ban(cls, telegram_id: int, bot: Bot, block_end_time: datetime.datetime = None, reason: str = None):
        block_end_time_string = ''
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user_obj = statement.scalar_one()
            user_obj.is_blocked = True
            if block_end_time is not None:
                user_obj.block_end_time = block_end_time
                block_end_time_string = block_end_time.strftime(STRFTIME_DEFAULT_FORMAT)

        await bot.send_message(chat_id=user_obj.telegram_id, text=MessageText.BAN_USER_NOTIFICATION.format(
            block_end_time=block_end_time_string or MessageText.PERMANENT_BLOCK_END_TIME,
            reason=reason or '',
        ))

    @classmethod
    async def subtract_voice_attempt(cls, telegram_id: int):
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user = statement.scalar_one()
            if user.is_audio_unlimited:
                return

            if user.audio_attempt_left:
                user.audio_attempt_left -= 1
            else:
                user.referral_audio_attempt_left -= 1

    @classmethod
    async def unban(cls, telegram_id: int):
        async with SessionLocal.begin() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            statement = await session.execute(query)
            user_obj = statement.scalar_one()
            user_obj.is_blocked = False
            user_obj.block_end_time = None
