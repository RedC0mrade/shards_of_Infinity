from sqlalchemy import Result, distinct, func, select, update
from sqlalchemy.orm import joinedload

from app.backend.core.models.card import Card, CardEffect, CardFaction
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.crud.base_service import BaseService
from app.backend.schemas.card import CreateCardSchema
from app.utils.exceptions.exceptions import CardInstanceError


class CardServices(BaseService):

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

    # async def get_hand_card(
    #     self,
    #     card_id: int,
    #     game_id: int,
    #     card_zone: str,
    #     player_state_id: int,
    # ) -> Card | None:
    #     stmt = (
    #         select(Card)
    #         .join(PlayerCardInstance, PlayerCardInstance.card_id == Card.id)
    #         .options(joinedload(Card.effects))
    #         .where(
    #             Card.id == card_id,
    #             PlayerCardInstance.player_state_id == player_state_id,
    #             PlayerCardInstance.zone == card_zone,
    #             PlayerCardInstance.game_id == game_id,
    #         )
    #     )
    #     result: Result = await self.session.execute(stmt)
    #     card = result.unique().scalar_one_or_none()

    #     return card

    async def change_card_zone(  # Переместить в PlayerCardInstance
        self,
        card_id: int,
        game_id: int,
        end_zone: CardZone,
        start_zone: CardZone,
    ) -> tuple[bool, str]:
        """Меняем положение карты"""
        self.logger.info(
            "Карта с id %s, меняем зону на %s",
            card_id,
            end_zone,
        )
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.card_id == card_id,
            PlayerCardInstance.game_id == game_id,
        )

        result: Result = await self.session.execute(stmt)
        instance: PlayerCardInstance = result.unique().scalar_one_or_none()

        if not instance:
            self.logger.error(
                "Не правильный id - %s, game id - %s",
                card_id,
                game_id,
            )
            raise CardInstanceError(message="Не правильно выбрана карта")

        if instance.zone != start_zone:
            self.logger.error("Не правильная зона - %s", instance.zone)
            raise CardInstanceError(message="Карта уже была разыграна")

        instance.zone = end_zone
        instance.position_on_market = None
        self.logger.info(
            "Зона карты изменена, теперь она %s позиция на рынке %s",
            instance.zone,
            instance.position_on_market,
        )
        await self.session.commit()

    async def card_order_check(
        self,
        player_state_id: int,
    ):
        """
        Проверяет, есть ли на столе карты трех фракций:
        """
        stmt = (
            select(func.count(distinct(Card.faction)))
            .select_from(PlayerCardInstance)
            .join(Card, PlayerCardInstance.card_id == Card.id)
            .where(
                PlayerCardInstance.player_state_id == player_state_id,
                PlayerCardInstance.zone == CardZone.IN_PLAY,
                Card.faction.in_(
                    [
                        CardFaction.WILDS,
                        CardFaction.HOMODEUS,
                        CardFaction.DEMIREALM,
                    ]
                ),
            )
            .group_by(Card.faction)
        )

        result = await self.session.execute(stmt)
        factions_present = result.scalars().all()

        return len(factions_present) == 3
