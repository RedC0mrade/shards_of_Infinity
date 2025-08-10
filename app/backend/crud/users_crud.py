from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.user import TelegramUser
from app.backend.schemas.users import UserCreateSchema


class UserServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_or_create_user(
        self,
        user_data: UserCreateSchema,
    ) -> TelegramUser:
        stmt = select(TelegramUser).where(TelegramUser.id == user_data.chat_id)
        result: Result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            return user

        user = TelegramUser(
            **user_data.model_dump(),
            id=user_data.chat_id,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
