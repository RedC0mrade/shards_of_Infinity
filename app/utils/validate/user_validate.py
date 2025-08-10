from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.core.models.user import TelegramUser


async def user_validate(
    chat_id: int,
    session: AsyncSession,
) -> TelegramUser:
    stmt = select(TelegramUser).where(TelegramUser.id == chat_id)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise
