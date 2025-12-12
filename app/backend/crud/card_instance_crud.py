from random import sample
from typing import TYPE_CHECKING
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardType, StartCardPlayer
from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.base_service import BaseService
from app.backend.schemas.play_state import CreatePlayStateSchema
from app.utils.exceptions.exceptions import Invulnerability
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
                self.logger.info(
                    "Создаем экземпляр карты для рынка - %s, зона - %s, позиция на рынке - %s, владелец - %s",
                    market.card_id,
                    market.zone,
                    market.position_on_market,
                    market.player_state_id,
                )
            else:
                card_instance = PlayerCardInstance(
                    player_state_id=None,
                    game_id=game_id,
                    card_id=card_id,
                    zone=CardZone.COMMON_DECK,
                    delete_mercenary=False,
                )
                self.logger.info(
                    "Создаем экземпляр карты - %s, владелец - %s",
                    card_instance.card_id,
                    card_instance.player_state_id,
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
        card_instance: PlayerCardInstance = result.unique().scalar_one_or_none()

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
        card_instanse = result.unique().scalar_one_or_none()

        if not card_instanse:
            self.logger.warning(
                "Нет состояния карты с id -%s", card_instanse_id
            )

        return card_instanse

    async def get_player_cards_instance_in_play(
        self,
        player_state: PlayerState,
    ) -> list[PlayerCardInstance]:
        """Получаем все карты игрока со стола, исключая чемпионов."""

        stmt = (
            select(PlayerCardInstance)
            .join(
                PlayerState,
                PlayerCardInstance.player_state_id == PlayerState.id,
            )
            .join(Card, Card.id == PlayerCardInstance.card_id)
            .where(
                PlayerState.player_id == player_state.player_id,
                PlayerCardInstance.zone == CardZone.IN_PLAY,
                Card.card_type != CardType.CHAMPION,
            )
        )

        result: Result = await self.session.execute(stmt)
        card_instances_in_play: list[PlayerCardInstance] = (
            result.unique().scalars().all()
        )
        self.logger.debug(
            "карты игрока со стола, исключая чемпионов. -%s",
            card_instances_in_play,
        )
        for card_instance in card_instances_in_play:
            self.logger.info(
                "🃏 Карта '%s' (тип: %s, фракция: %s) находится в зоне %s.",
                card_instance.card.name,
                card_instance.card.card_type,
                card_instance.card.faction,
                card_instance.zone,
            )
        stmt = (
            select(PlayerCardInstance)
            .join(
                PlayerState,
                PlayerCardInstance.player_state_id == PlayerState.id,
            )
            .join(Card, Card.id == PlayerCardInstance.card_id)
            .where(
                PlayerState.player_id == player_state.player_id,
                PlayerCardInstance.zone == CardZone.HAND,
            )
        )
        result: Result = await self.session.execute(stmt)
        card_instances_hand: list[PlayerCardInstance] = (
            result.unique().scalars().all()
        )
        self.logger.debug(
            "карты игрока руки. -%s",
            card_instances_hand,
        )
        for card_instance in card_instances_hand:
            self.logger.info(
                "🃏 Карта '%s' (тип: %s, фракция: %s) находится в зоне %s.",
                card_instance.card.name,
                card_instance.card.card_type,
                card_instance.card.faction,
                card_instance.zone,
            )
        return card_instances_in_play + card_instances_hand

    async def change_zone_of_cards(
        self,
        card_instances: list[PlayerCardInstance],
    ) -> list[PlayerCardInstance]:
        """Меняем зону карты в PlayerCardInstance"""
        for card_instance in card_instances:
            card_instance.zone = CardZone.DISCARD
            self.logger.info(
                "🃏 Карта '%s' (тип: %s, фракция: %s) находится в зоне %s.",
                card_instance.card.name,
                card_instance.card.card_type,
                card_instance.card.faction,
                card_instance.zone,
            )
        await self.session.flush()  # наверное не нужно, проверить

    async def zetta_check(self, player_state: PlayerState):
        """Проверка на неуязвимость."""

        stmt = (
            select(PlayerCardInstance)
            .join(
                PlayerState,
                PlayerState.id == PlayerCardInstance.player_state_id,
            )
            .join(Game, Game.id == PlayerCardInstance.game_id)
            .join(Card, Card.id == PlayerCardInstance.card_id)
        ).where(
            Game.status == GameStatus.IN_PROGRESS,
            PlayerState.player_id == player_state.player_id,
            PlayerCardInstance.zone == CardZone.IN_PLAY,
            Card.name == "Зетта, энкриптор",
            Game.non_active_player_id == player_state.player_id,
        )
        result: Result = await self.session.execute(stmt)
        zetta = result.scalar_one_or_none()
        self.logger.warning("Проверка zetta_check - %s", zetta)
        if zetta:
            raise Invulnerability(
                message="⚔️ Невозможно атаковать противника, разыграна карта чемпиона Зетта, энкриптор"
            )

    async def take_card_to_hand(
        self,
        player_state: PlayerState,
        number_cards: int,
    ):
        """Добавляем карты в руку игрока для effects"""

        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.player_state_id == player_state.id,
            PlayerCardInstance.zone == CardZone.PLAYER_DECK,
        )
        result: Result = await self.session.execute(stmt)
        card_instanses: list[PlayerCardInstance] = (
            result.unique().scalars().all()
        )
        self.logger.info("Карты игрока в колоде:")
        for instanse in card_instanses:
            self.logger.info("         Карта %s", instanse.id)

        if len(card_instanses) < number_cards:
            self.logger.info(
                "Нужно взять карт - %s, карт в колоде -%s",
                number_cards,
                len(card_instanses),
            )
            for card_instanse in card_instanses:
                card_instanse.zone = CardZone.HAND

            stmt = select(PlayerCardInstance).where(
                PlayerCardInstance.player_state_id == player_state.id,
                PlayerCardInstance.zone == CardZone.DISCARD,
            )
            result: Result = await self.session.execute(stmt)

            discard_cards: list[PlayerCardInstance] = (
                result.unique().scalars().all()
            )
            self.logger.info(
                "Количество карт в сбросе у игрока - %s",
                len(discard_cards),
            )
            self.logger.info("Переносим карты в колоду:")
            for card in discard_cards:
                self.logger.info(
                    "      Карта c id- %s",
                    card.id,
                )
                card.zone = CardZone.PLAYER_DECK

            missing_cards = number_cards - len(card_instanses)
            self.logger.info(
                "Количество карт которые нужно добрать - %s",
                missing_cards,
            )

            cards_to_hand: list[PlayerCardInstance] = sample(
                discard_cards,
                missing_cards,
            )
            self.logger.info("Карты Которые переходят в руку:")

            for card in cards_to_hand:
                self.logger.info("         id - %s", card.id)
                card.zone = CardZone.HAND
        else:
            cards_to_hand = sample(card_instanses, number_cards)
            self.logger.info("Карты (id) которые переходят в руку:")
            for card in cards_to_hand:
                card.zone = CardZone.HAND
                
                self.logger.info(
                "      id - %s", card.id
            )
        await self.session.commit()
