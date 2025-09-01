from random import choice
from fastapi import HTTPException, status
from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.utils.logger import get_logger


class HandServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def get_hand(self, player_id: int):
        """Страртовая рука перед началом хода."""

        stmt = (
            select(PlayerCardInstance)
            .join(
                PlayerState,
                PlayerCardInstance.player_state_id == PlayerState.id,
            )
            .where(
                PlayerState.player_id == player_id,
                PlayerCardInstance.zone == CardZone.DECK,
            )
        )
        result: Result = await self.session.execute(stmt)
        card_instance = result.scalars().all()
        if len(card_instance < 5):
            stmt = (
                select(PlayerCardInstance)
                .join(
                    PlayerState,
                    PlayerCardInstance.player_state_id == PlayerState.id,
                )
                .where(
                    PlayerState.player_id == player_id,
                    PlayerCardInstance.zone == CardZone.DISCARD,
                )
            )
            result: Result = await self.session.execute(stmt)
            discards = result.scalars().all()
            
            while card_instance < 5:
                card_instance += choice(discards)
        
        stmt = 