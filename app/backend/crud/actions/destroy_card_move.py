from sqlalchemy import Result, or_, select
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import CardZone, PlayerCardInstance
from app.backend.crud.base_service import BaseService


class DestroyCardService(BaseService):

    async def destroy_card(
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
        result: Result = self.session.execute(stmt)
        card_instances = result.unique().scalars().all()

        return card_instances