from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.crud.users_crud import UserServices
from app.backend.factories.database import db_helper


def get_user_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserServices:
    return UserServices(session=session)