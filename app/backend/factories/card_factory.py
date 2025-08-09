from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.crud.card_crud import CardServices
from app.backend.factories.database import db_helper


def get_card_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> CardServices:
    return CardServices(session=session)
