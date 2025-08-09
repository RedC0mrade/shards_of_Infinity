from pydantic import BaseModel, PositiveInt

from app.backend.core.models.game import GameStatus


class CreateGameSchema(BaseModel):

    player1_id: PositiveInt
    # active_player_id: PositiveInt = player1_id
    invite_token: str

class InvateGameSchema(CreateGameSchema):

    player2_id: PositiveInt
    status: GameStatus

class GameSchems(InvateGameSchema):

    id: PositiveInt