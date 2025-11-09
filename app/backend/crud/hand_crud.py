from random import choice, sample
from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.base_service import BaseService
from app.utils.logger import get_logger


class HandServices(BaseService):

    async def get_cards_in_zone(
        self,
        game_id: int,
        player_id: int,
        card_zone: CardZone,
    ) -> list[PlayerCardInstance]:
        """Получаем карты, из определенной зоны"""

        self.logger.info(
            "Полчение карт для игрока с id %s в зоне %s",
            player_id,
            card_zone,
        )
        stmt = (
            select(PlayerCardInstance)
            .join(
                PlayerState,
                PlayerCardInstance.player_state_id == PlayerState.id,
            )
            .where(
                PlayerState.game_id == game_id,
                PlayerState.player_id == player_id,
                PlayerCardInstance.zone == card_zone,
            )
        )
        result: Result = await self.session.execute(stmt)
        hand = result.scalars().all()

        for card in hand:
            self.logger.info(
                "Карты игрока id - %s, zone - %s",
                card.id,
                card.zone,
            )
        return hand

    async def get_cards_in_play(
        self,
        card_zone: CardZone,
        game_id: int,
    ) -> list[PlayerCardInstance]:
        """Получаем разыгранные карты."""
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.game_id == game_id,
            PlayerCardInstance.zone == card_zone,
        )

        result: Result = await self.session.execute(stmt)
        cards = result.scalars().all()
        for card in cards:
            self.logger.info(
                "Картa id - %s, zone - %s",
                card.id,
                card.zone,
            )
        return cards

    async def create_hand(
        self,
        player_id: int,
        hand_count: int = 5,
    ) -> list[PlayerCardInstance]:
        """Рука после окончания хода."""

        self.logger.info(
            "Создание руки для игрока с id %s",
            player_id,
        )
        stmt = (
            select(PlayerCardInstance)
            .join(
                PlayerState,
                PlayerCardInstance.player_state_id == PlayerState.id,
            )
            .where(
                PlayerState.player_id == player_id,
                PlayerCardInstance.zone == CardZone.PLAYER_DECK,
            )
        )
        result: Result = await self.session.execute(stmt)
        deck = result.scalars().all()

        self.logger.info("Колода игрока %s", deck)

        if len(deck) < hand_count:

            self.logger.info(
                "Карт в колоде меньше %s: %s",
                hand_count,
                len(deck),
            )

            stmt = (
                select(PlayerCardInstance)
                .join(
                    PlayerState,
                    PlayerCardInstance.player_state_id == PlayerState.id,
                )
                .where(
                    PlayerState.player_id == player_id,
                    PlayerCardInstance.zone == CardZone.DISCARD,
                )
            )
            result: Result = await self.session.execute(stmt)
            discards: list[PlayerCardInstance] = result.scalars().all()

            self.logger.info("Карты в бросе %s", discards)

            hand_cards = deck

            while len(hand_cards) < hand_count:

                self.logger.info(
                    "Увеличиваем руку из 5 карт. Карты на данный момент == %s",
                    hand_cards,
                )

                card = choice(discards)
                hand_cards.append(card)
                discards.remove(card)

            for card in discards:
                card.zone = CardZone.PLAYER_DECK

        else:
            hand_cards = sample(
                deck,
                hand_count,
            )
            self.logger.info("Карты взятые в руку - %s", hand_cards)

        for card in hand_cards:
            card.zone = CardZone.HAND

        # self.session.add_all(discards + hand_cards)
        # await self.session.commit()
        self.logger.info("Финальная рука: %s", hand_cards)

        # return hand_cards
