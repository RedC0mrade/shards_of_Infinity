from sqlalchemy import Result, or_, select
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import CardZone, PlayerCardInstance
from app.backend.crud.base_service import BaseService


class DestroyCardService(BaseService):

    async def get_card_for_destroy(
        self,
        game_id: int,
        player_state_id: int,
    ) -> list[PlayerCardInstance]:

        stmt = (
            select(PlayerCardInstance)
            .where(
                or_(
                    PlayerCardInstance.zone == CardZone.DISCARD,
                    PlayerCardInstance.zone == CardZone.HAND,
                ),
                PlayerCardInstance.player_state_id == player_state_id,
                PlayerCardInstance.game_id == game_id,
            )
        )
        result: Result = await self.session.execute(stmt)
        card_instances = result.unique().scalars().all()

        return card_instances
    
    async def destroy_card(self, card_instance_id: int):
        """Уничтожение карты противника."""

        stmt = select(PlayerCardInstance).where(PlayerCardInstance.id == card_instance_id)

        result: Result = await self.session.execute(stmt)
        card_instance = result.unique().scalar_one_or_none()
        if not card_instance:
            raise