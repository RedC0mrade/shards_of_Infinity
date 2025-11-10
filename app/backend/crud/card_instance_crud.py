from random import sample
from typing import TYPE_CHECKING
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, StartCardPlayer
from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.base_service import BaseService
from app.backend.schemas.play_state import CreatePlayStateSchema
from app.utils.logger import get_logger


class CardInstanceServices(BaseService):

    async def create_card_instance_for_all_cards(
        self,
        game_id: int,
        count: int = 6,
    ):
        self.logger.info(
            "Создаем стартовые экземпляры карт для игры с id - %s",
            game_id,
        )
        stmt = select(Card.id).where(Card.start_card == StartCardPlayer.OTHER)
        result: Result = await self.session.execute(stmt)
        available_cards_id = result.scalars().all()

        self.logger.info(
            "Получаем id карт - %s",
            available_cards_id,
        )
        if not available_cards_id:
            self.logger.error(
                "Нет доступных карт для рынка в игре %s",
                game_id,
            )
            return []

        if len(available_cards_id) < count:
            self.logger.warning(
                "Доступных карт (%s) меньше, чем требуется (%s). Используем все карты.",
                len(available_cards_id),
                count,
            )
            count = len(available_cards_id)

        market_cards_ids: list[int] = sample(available_cards_id, count)

        cards_instances = []
        market_cards_instance = []
        position_on_market = 0
        for card_id in available_cards_id:
            if card_id in market_cards_ids:
                position_on_market += 1
                market = PlayerCardInstance(
                    game_id=game_id,
                    position_on_market=position_on_market,
                    card_id=card_id,
                    zone=CardZone.MARKET,
                )
                market_cards_instance.append(market)

            else:
                card_instance = PlayerCardInstance(
                    player_state_id=None,
                    game_id=game_id,
                    card_id=card_id,
                    zone=CardZone.COMMON_DECK,
                    delete_mercenary=False,
                )
                self.logger.info(
                    "Создаем экземпляр карты - %s", card_instance.card_id
                )
                cards_instances.append(card_instance)
        self.session.add_all(cards_instances)
        self.session.add_all(market_cards_instance)
        # await self.session.commit()

    async def get_card_instance_in_some_card_zone(
        self,
        card_id: int,
        game_id: int,
        card_zone: CardZone,
    ) -> PlayerCardInstance:
        """Получаем информацию о состоянии карты в определенной зоне."""

        self.logger.info(
            "card_id - %s, game_id - %s, card_zone - %s",
            card_id,
            game_id,
            card_zone,
        )
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.card_id == card_id,
            PlayerCardInstance.game_id == game_id,
            PlayerCardInstance.zone == card_zone,
        )
        result: Result = await self.session.execute(stmt)
        card_instance: PlayerCardInstance = result.scalar_one_or_none()

        if not card_instance:
            self.logger.warning(
                "card_instance c card_id -%s, game_id - %s и card_zone - %s  не найден",
                card_id,
                game_id,
                card_zone,
            )
            return None
        self.logger.info(
            "Получен card_instance с картой - %s",
            card_instance.card.name,
        )

        return card_instance

    async def get_card_instance_for_id(
        self,
        card_instanse_id: int,
    ) -> PlayerCardInstance:

        self.logger.info("Получаем id - %s состояния карты", card_instanse_id)
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.id == card_instanse_id
        )

        result: Result = await self.session.execute(stmt)
        card_instanse = result.scalar_one_or_none()

        if not card_instanse:
            self.logger.warning("Нет состояния карты с id -%s", card_instanse_id)

        return card_instanse

    async def get_all_card_instance(
            self,
            player_state: PlayerState,
            game: Game,
    ) -> list[PlayerCardInstance]:
        """Получаем все карты игрока из руки и со стола, исключая чемпионов."""

        stmt = select(PlayerCardInstance).join((
                    PlayerState,
                    PlayerCardInstance.player_state_id == PlayerState.id,
                ).where(PlayerState.player_id == player_state.player_id, PlayerCardInstance.zone == CardZone.IN_PLAY)
                )