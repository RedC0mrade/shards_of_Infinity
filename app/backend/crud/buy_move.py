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
        mercenary: bool,
    ):
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
                f"Недостаточно кристалов({player_state.crystals}) "
                f"для покупки карты {card.name} за {card.crystals_cost}"
            )

        if card_instance.zone != CardZone.MARKET:
            self.logger.warning(
                "Не правильная зона карты %s",
                card_instance.zone,
            )
            return "ошибка зоны карты"

        player_state.crystals -= card.crystals_cost
        self.logger.info(
            "оставщееся количество кристалов",
            player_state.crystals,
        )


# Покупка карты с рынка
# 1 Проверяем на рынке ли карта
# 2 проверяем хватает ли кристалов
# 3 отнимаем кристалы из банка игрока
# 4 проверяем наёмлик это или нет
# 4.1 разыгрываем
# 4.2 переносим карту в сброс
# 5 переносим карту в сброс
