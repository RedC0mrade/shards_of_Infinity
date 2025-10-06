from pydantic import BaseModel

class CreatePlayStateSchema(BaseModel):
    game_id: int
    player_id: int
    health: int = 50
    mastery: int
    crystals: int = 0
    power: int = 0
    # deck_count: int = 0
    # discard_count: int = 0
    # hand_count: int = 0
    # is_defeated: bool = False

class PlayStateSchema(BaseModel):
    id: int