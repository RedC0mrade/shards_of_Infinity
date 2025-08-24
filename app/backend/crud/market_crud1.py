import random
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card
from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.market import MarketSlot
from app.backend.core.models.play_card_instance import PlayerCardInstance
from app.backend.core.models.player_state import PlayerState


class MarketServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create_market(
        self,
        game: Game,
        count: int = 6,
    ):
        stmt = select(Card.id).where(Card.start_card == False)
        result: Result = await self.session.execute(stmt)
        available_cards = result.scalars().all()

        available_cards_ids: list[int] = random.sample(available_cards, count)
        market_cards = [
            MarketSlot(
                game_id=game.id,
                position=i + 1,
                card_id=available_cards_ids[i],
            )
            for i in range(count)
        ]

        self.session.add_all(market_cards)
        await self.session.commit()
        await self.session.refresh(market_cards)
        return market_cards
