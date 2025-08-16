from pydantic import BaseModel


class CreatePlayStateSchema(BaseModel):
    game_id: int
    player_id: int
    health: int
    mastery: int
    crystals: int
    power: int
    deck_count: int
    discard_count: int
    hand_count: int
    is_defeated: bool

class PlayStateSchema(BaseModel):
    id: int