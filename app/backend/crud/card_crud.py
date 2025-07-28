from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardEffect
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
            CardEffect(
                action=effect.action,
                value=effect.value,
                effect_type=effect.effect_type,
                condition_type=effect.condition_type,
                condition_value=effect.condition_value,
            )
            for effect in card_data.effects
        ]
        card = Card(
            name=card_data.name,
            crystals_cost=card_data.crystals_cost,
            description=card_data.description,
            shield=card_data.shield,
            champion_health=card_data.champion_health,
            card_type=card_data.card_type,
            faction=card_data.faction,
            icon=card_data.icon,
            effects=effects,
        )

        self.session.add(card)
        await self.session.commit()
        await self.session.refresh(card)

        return card
