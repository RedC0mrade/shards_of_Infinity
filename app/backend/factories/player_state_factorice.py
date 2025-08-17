from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.factories.database import db_helper


def get_player_state_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> PlayerStateServices:
    return PlayerStateServices(session=session)