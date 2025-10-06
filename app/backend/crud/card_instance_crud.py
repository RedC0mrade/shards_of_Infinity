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

    async def create_card_instance_for_all_cards(
        self,
        game_id: int,
    ):
        self.logger.info(
            "Создаем стартовые экземпляры карт для игры с id - %s",
            game_id,
        )
        stmt = select(Card.id).where(Card.start_card == False)
        result: Result = await self.session.execute(stmt)
        cards_ids = result.scalars().all
        self.logger.info(
            "Получаем id карт - %s",
            cards_ids,
        )
        cards_instances = []
        for card_id in cards_ids:
            card_instance = PlayerCardInstance(
                player_state_id=None,
                game_id=game_id,
                card_id=card_id,
                zone=CardZone.COMMON_DECK,
                delete_mercenamy=False,
            )
            self.logger.info(
                "Создаем экземпляр карты - %s",
                )
            cards_instances.append(card_instance)
        self.session.add_all(cards_instances)
        await self.session.commit()

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
        card_instance: PlayerCardInstance = result.scalar_one_or_none()

        if not card_instance:
            self.logger.warning(
                "card_instance c card_id -%s, player_state_id - %s и card_zone - %s  не найден",
                card_id,
                player_state_id,
                card_zone,
            )
            return None
        self.logger.info(
            "Получен card_instance с картой - %s",
            card_instance.card.name,
        )
        self.logger.debug(
            "Обратить внимание. Где то тут баг должна быть зона маркет %s",
            card_instance.zone,
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
            self.logger.warning("Нет состояния карты с id -%s", card_instanse)

        return card_instanse
