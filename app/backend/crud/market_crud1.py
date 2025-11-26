from random import sample
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.base_service import BaseService
from app.utils.exceptions.exceptions import MarketError


class MarketServices(BaseService):

    async def get_market_cards(self, game_id: int) -> list[PlayerCardInstance]:
        """Получаем карты с рынка"""
        self.logger.info(
            "Получаем Маркет слоты по game id == %s",
            game_id,
        )

        stmt = (
            select(PlayerCardInstance)
            .where(
                PlayerCardInstance.game_id == game_id,
                PlayerCardInstance.zone == CardZone.MARKET,
            )
            .order_by(PlayerCardInstance.position_on_market)
        )

        result: Result = await self.session.execute(stmt)
        market_cards = result.unique().scalars().all()

        if not market_cards:
            self.logger.warning(
                "Нет карт на рынке у игры с id == %s",
                game_id,
            )
            raise MarketError(message="❌ Нет карт на рынке.")
        return market_cards

    # async def buy_market_card(
    #     self,
    #     card_instance_id: int,
    #     player_state: PlayerState,
    # ):
    #     """Покупка карты с рынка"""

    #     self.logger.info(
    #         "Покупка карты с id %s рынка",
    #         card_instance_id,
    #     )


# Покупка карты
# - выбираем карту
# - проверяем хватает ли кристалов
# - переносим карты в сброс
# - если наемник спрашиваем куда её перенести на стол или в брос
# добавляем карту на рынок в тоже место
