from sqlalchemy import Result, select
from app.backend.core.models.card import Card
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import CardZone, PlayerCardInstance
from app.backend.crud.base_service import BaseService


class MarketService(BaseService):

    async def get_cards_for_less_than_six_crystals(self, game_id: int):

        stmt = (
            select(PlayerCardInstance)
            .join(Card, Card.id == PlayerCardInstance.card_id)
            .where(
                PlayerCardInstance.game_id == game_id,
                PlayerCardInstance.zone == CardZone.MARKET,
                Card.crystals_cost <= 6,
            )
        )

        result: Result = await self.session.execute(stmt)
        cards: list[int]