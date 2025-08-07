from pydantic import BaseModel

from app.backend.core.models.game import GameStatus


class CreateGameSchema(BaseModel):

    player1_id: int
    invite_token: str

class GameSchema(CreateGameSchema):

    id: int
    player2_id: int
    active_player_id: int
    status: GameStatus