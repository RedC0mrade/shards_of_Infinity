from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card


class CardServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all_cards_in_the_deck(self) -> list[Card]:
        stmt = select(Card)
        result: Result = await self.session.execute(stmt)
        cards = result.scalar().all()
        return list(cards)
