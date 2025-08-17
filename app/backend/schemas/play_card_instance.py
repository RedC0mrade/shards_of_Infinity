from pydantic import BaseModel

from app.backend.core.models.play_card_instance import CardZone


class CreatePCISchema(BaseModel):
    player_state_id: int
    card_id: int
    zone: CardZone = CardZone.DECK
    order_in_zone : int = 0
    is_exhausted: bool = False
    was_played_this_turn: bool = False
