from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.user import TelegrammUser
from app.backend.schemas.users import UserCreateSchema


class UserServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_or_create_user(
        self,
        user_data: UserCreateSchema
    ) -> TelegrammUser:
        stmt = select(TelegrammUser).where(
            TelegrammUser.telegramm_id == user_data.telegramm_id
        )
        result: Result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            return user
        user = TelegrammUser(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user