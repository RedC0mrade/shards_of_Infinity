import random
from typing import TYPE_CHECKING
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card
from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.schemas.play_state import CreatePlayStateSchema
from app.utils.logger import get_logger


class CardInstanceServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def get_card_instance_in_some_card_zone(
        self,
        card_id: int,
        player_state_id: int,
        card_zone: CardZone,
    ) -> PlayerCardInstance | str:
        """Получаем информацию о состоянии карты в определенной зоне."""

        self.logger.info(
            "card_id - %s, player_state_id - %s, card_zone - %s",
            card_id,
            player_state_id,
            card_zone,
        )
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.card_id == card_id,
            PlayerCardInstance.player_state_id == player_state_id,
            PlayerCardInstance.zone == card_zone,
        )
        result: Result = await self.session.execute(stmt)
        card_instance = result.scalar_one_or_none()

        if not card_instance:
            self.logger.info(
                "card_instance c card_id -%s, player_state_id - %s и card_zone - %s  не найден",
                card_id,
                player_state_id,
                card_zone,
            )
            return "Карта в руке не найдена"
        self.logger.info(
            "Получен card_instance с картой - %s",
            card_instance.card.name,
        )

        return card_instance

    async def get_card_inctance_for_id(
        self,
        card_instanse_id: int,
    ) -> PlayerCardInstance:

        self.logger.info("Получаем id - %s состояния карты", card_instanse_id)
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.id == card_instanse_id
        )

        result: Result = self.session.execute(stmt)
        card_instanse = result.scalar_one_or_none()

        if not card_instanse:
            self.logger.warning("Нет состояния казты с id -%s", card_instanse)

        return card_instanse
