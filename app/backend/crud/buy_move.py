from random import choice
from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardAction, EffectType
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.utils.logger import get_logger


class BuyServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def buy_card_from_market(
        self,
        player_state: PlayerState,
        card: Card,
        card_instance: PlayerCardInstance,
        game: Game,
        player_id: int,
    ) -> tuple[bool, str]:
        """Игрок покупает карту с рынка"""
        self.logger.info(
            "Игрок id - %s покупает карту - %s, в игре id - %s, зоне - %s",
            player_id,
            card.name,
            game.id,
            card_instance.zone,
        )
        if player_state.crystals < card.crystals_cost:
            self.logger.warning(
                "Недостаточно кристалов (%s), для покупки необходимо - %s",
                player_state.crystals,
                card.crystals_cost,
            )
            return (
                False,
                (
                    f"Недостаточно кристалов💎 Вы имеете"
                    f" - {player_state.crystals} "
                    f"для покупки карты🃏 {card.name} за "
                    f"{card.crystals_cost} кристалов💎"
                ),
            )

        if card_instance.zone != CardZone.MARKET:
            self.logger.warning(
                "Не правильная зона карты %s",
                card_instance.zone,
            )
            return (False, f"Не правильно выбрана карта🃏")

        player_state.crystals -= card.crystals_cost
        self.logger.info(
            "оставщееся количество кристалов - %s",
            player_state.crystals,
        )
        card_instance.zone = CardZone.DISCARD
        card_instance.player_state_id = player_state.id
        position_on_market = card_instance.position_on_market
        card_instance.position_on_market = None
        await self.replacement_cards_from_the_market(
            game_id=game.id,
            position_on_market=position_on_market,
        )
        await self.session.commit()
        return (True, "")

    async def replacement_cards_from_the_market(
        self,
        game_id: int,
        position_on_market: int,
    ):
        "Заменяем карту купленную с рынка."
        self.logger.info("Делаем замену карты на рынке")
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.game_id == game_id,
            PlayerCardInstance.zone == CardZone.COMMON_DECK,
        )
        result: Result = await self.session.execute(stmt)
        available_cards_instance_id = result.scalars().all()
        self.logger.info(
            "Получаем id состояния карты в общей колоде- %s",
            available_cards_instance_id,
        )
        if not available_cards_instance_id:
            self.logger.error(
                "Нет доступных состояний карт для рынка в игре %s",
                game_id,
            )
            return []

        replacement_card_instance: PlayerCardInstance = choice(
            available_cards_instance_id
        )
        self.logger.info(
            "Получаем id состояния карты на замену - %s",
            replacement_card_instance.id,
        )

        replacement_card_instance.zone = CardZone.MARKET
        replacement_card_instance.position_on_market = position_on_market
