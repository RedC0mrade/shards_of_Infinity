from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.core.models.user import TelegrammUser


async def user_validate(
    telegram_id: int,
    session: AsyncSession,
) -> TelegrammUser:
    stmt = select(TelegrammUser).where(
        TelegrammUser.telegramm_id == telegram_id
        )
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise 