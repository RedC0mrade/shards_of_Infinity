from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.user import TelegrammUser


class UserSer:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_or_create_user(
        self,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> TelegrammUser:
        stmt = select(TelegrammUser).where(
            TelegrammUser.telegramm_id == user_id
        )
        result: Result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            return user
        user = TelegrammUser(
            telegramm_id=user_id,
            first_name=first_name,
            last_name=last_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)