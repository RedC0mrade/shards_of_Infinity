from sqlalchemy import Result, select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardEffect
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.schemas.card import CreateCardSchema
from app.utils.logger import get_logger


class CardServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def get_all_cards_in_the_deck(self) -> list[Card]:
        stmt = select(Card)
        result: Result = await self.session.execute(stmt)
        cards = result.scalars().unique().all()
        return list(cards)

    async def create_card(self, card_data: CreateCardSchema) -> Card:
        effects = [
            CardEffect(**effect.model_dump()) for effect in card_data.effects
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
        stmt = select(Card).where(Card.id == card_id)
        result: Result = await self.session.execute(stmt)
        card = result.unique().scalar_one_or_none()
        return card

    async def get_hand_card(
        self,
        card_id: int,
        game_id: int,
        card_zone: str,
        player_state_id: int,
    ) -> Card | None:
        stmt = (
            select(Card)
            .join(PlayerCardInstance, PlayerCardInstance.card_id == Card.id)
            .options(joinedload(Card.effects))
            .where(
                Card.id == card_id,
                PlayerCardInstance.player_state_id == player_state_id,
                PlayerCardInstance.zone == card_zone,
                PlayerCardInstance.game_id == game_id,
            )
        )
        result: Result = await self.session.execute(stmt)
        card = result.unique().scalar_one_or_none()

        return card

    async def change_card_zone(
        self,
        card_id: int,
        game_id: int,
        card_zone: CardZone,
    ):
        """Меняем положение карты"""
        self.logger.info(
            "Карта с id %s, меняем зону на %s",
            card_id,
            card_zone,
        )
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.card_id == card_id,
            PlayerCardInstance.game_id == game_id,
        )

        result: Result = await self.session.execute(stmt)
        instance: PlayerCardInstance = result.scalar_one_or_none()

        if not instance:
            self.logger.error(
                "Не правильный id - %s, game id - %s",
                card_id,
                game_id,
            )
            return
        if instance.zone not in (CardZone.HAND, CardZone.MARKET): # ПЕРЕДЕЛАТЬ!!!
            self.logger.warning("Не правильная зона - %s", instance.zone)
            return

        instance.zone = card_zone
        self.logger.info("Зона карты изменена, теперь она %s", instance.zone)
        await self.session.commit()
