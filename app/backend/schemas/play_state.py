from pydantic import BaseModel

class CreatePlayStateSchema(BaseModel):
    game_id: int
    player_id: int
    health: int = 50
    mastery: int
    crystals: int = 0
    power: int = 0


class PlayStateSchema(BaseModel):
    id: int