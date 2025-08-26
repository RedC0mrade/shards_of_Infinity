import random
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card
from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.market import MarketSlot
from app.backend.core.models.play_card_instance import PlayerCardInstance
from app.backend.core.models.player_state import PlayerState
from app.utils.logger import get_logger


class MarketServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def create_market(
        self,
        game: Game,
        count: int = 6,
    ) -> list[MarketSlot]:
        self.logger.info(
            "Создание рынка для игры %s (кол-во карт %s)",
            game.id,
            count,
        )
        stmt = select(Card.id).where(Card.start_card == False)
        result: Result = await self.session.execute(stmt)
        available_cards = result.scalars().all()

        if not available_cards:
            self.logger.error(
                "Нет доступных карт для рынка в игре %s",
                game.id,
            )
            return []
        if len(available_cards) < count:
            self.logger.warning(
                "Доступных карт (%s) меньше, чем требуется (%s). Используем все карты.",
                len(available_cards), count,
            )
            count = len(available_cards)

        available_cards_ids: list[int] = random.sample(available_cards, count)
        market_cards = [
            MarketSlot(
                game_id=game.id,
                position=i + 1,
                card_id=available_cards_ids[i],
            )
            for i in range(count)
        ]

        self.session.add_all(market_cards)
        await self.session.flush()         # Не забыть, что нужно закоммитить
        self.logger.info(
            "Рынок для игры %s создан. Карты: %s",
            game.id, available_cards_ids,
        )
        return market_cards
