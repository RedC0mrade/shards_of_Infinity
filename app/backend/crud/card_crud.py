from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardEffect
from app.backend.core.models.play_card_instance import CardZone, PlayerCardInstance
from app.backend.schemas.card import CreateCardSchema


class CardServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all_cards_in_the_deck(self) -> list[Card]:
        stmt = select(Card)
        result: Result = await self.session.execute(stmt)
        cards = result.scalars().unique().all()
        return list(cards)

    async def create_card(self, card_data: CreateCardSchema) -> Card:
        effects = [
            CardEffect(**effect.model_dump())
            for effect in card_data.effects
        ]
        card = Card(
            **card_data.model_dump(exclude={"effects"}),
            effects=effects,
        )
        self.session.add(card)
        await self.session.commit()
        await self.session.refresh(card)

        return card

    async def create_all_cards(
        self,
        cards_data: list[CreateCardSchema],
    ) -> list[Card]:
        cards = []
        for card in cards_data:
            cards.append(await self.create_card(card))
        return cards

    async def get_card(self, card_id: int) -> Card:
        stmt = select(Card).where(Card.id==card_id)
        result: Result = await self.session.execute(stmt)
        card = result.unique().scalar_one_or_none()
        return card
    
    async def get_hand_card(self, card_id: int) -> Card | None:
        stmt = (
            select(Card)
            .join(PlayerCardInstance, PlayerCardInstance.card_id == Card.id)
            .options(joinedload(Card.effects))
            .where(
                Card.id == card_id,
                PlayerCardInstance.zone == CardZone.HAND,
            )
        )
        result: Result = await self.session.execute(stmt)
        card = result.unique().scalar_one_or_none()
        return card