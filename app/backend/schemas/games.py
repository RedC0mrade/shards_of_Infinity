from pydantic import BaseModel, PositiveInt

from app.backend.core.models.game import GameStatus


class CreateGameSchema(BaseModel):

    player1_id: PositiveInt
    invite_token: str

class InvateGameSchema(CreateGameSchema):

    player2_id: PositiveInt
    status: GameStatus

class GameSchems(InvateGameSchema):

    id: PositiveInt