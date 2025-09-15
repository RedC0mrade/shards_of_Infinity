from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardAction, EffectType
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.effects_crud import EffectExecutor
from app.utils.logger import get_logger


class MoveServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def make_move(
        self,
        card: Card,
        game: Game,
        player_id: int,
        player_state: PlayerState,
    ):
        self.logger.info(
            "Игрок с id - %s делает ход картой - %s, c эффектами - %s в игре с id - %s",
            player_id,
            card.name,
            card.effects,
            game.id,
        )
        executor = EffectExecutor(player_state, game, self.session)

        for effect in card.effects:
            await executor.execute(effect)

        await self.session.commit()
