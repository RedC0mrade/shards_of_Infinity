from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.crud.games import GameServices
from app.backend.crud.users_crud import UserServices
from app.backend.factories.database import db_helper


def get_game_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> GameServices:
    return GameServices(session=session)