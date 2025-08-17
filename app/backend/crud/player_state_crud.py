from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import PlayerCardInstance
from app.backend.core.models.player_state import PlayerState
from app.backend.schemas.play_state import CreatePlayStateSchema

if TYPE_CHECKING:
    from app.backend.core.models.game import Game


class PlayerStateServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create_play_state(
        self,
        play_datas: list[CreatePlayStateSchema],
    ) -> list[PlayerState]:
        play_states = [
            PlayerState(
                **play_data.model_dump(),
                cards=[
                    PlayerCardInstance(
                        card_id=card_id,
                    )
                    for card_id in range(1, 11)
                ]
            )
            for play_data in play_datas
        ]

        async with self.session.begin():
            self.session.add_all(play_states)

        return play_states

    def assign_mastery(self, game: Game) -> list[CreatePlayStateSchema]:
        """Назначает mastery игрокам в зависимости от того, чей ход первый."""
        player1_id = game.player1_id
        player2_id = game.player2_id

        if game.active_player_id == player1_id:
            return [
                CreatePlayStateSchema(
                    game_id=game.id,
                    player_id=player1_id,
                    mastery=0,
                ),
                CreatePlayStateSchema(
                    game_id=game.id,
                    player_id=player2_id,
                    mastery=1,
                ),
            ]
        else:
            return [
                CreatePlayStateSchema(
                    game_id=game.id,
                    player_id=player1_id,
                    mastery=1,
                ),
                CreatePlayStateSchema(
                    game_id=game.id,
                    player_id=player2_id,
                    mastery=0,
                ),
            ]
