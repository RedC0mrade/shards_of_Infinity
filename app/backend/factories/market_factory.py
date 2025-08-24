from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.crud.market_crud1 import MarketServices
from app.backend.factories.database import db_helper


def get_market_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> MarketServices:
    return MarketServices(session=session)