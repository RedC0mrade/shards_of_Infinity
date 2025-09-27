from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardAction, EffectType
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_crud import CardServices
from app.backend.crud.executors.effects_executor import EffectExecutor
from app.backend.crud.executors.ps_count_executor import PlayStateExecutor
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
        card_id: int,
    ):
        pass
