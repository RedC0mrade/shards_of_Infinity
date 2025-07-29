from pydantic import BaseModel, NonNegativeInt
from typing import Annotated, List
from app.backend.core.models.card import (
    CardAction,
    CardFaction,
    CardType,
    ConditionType,
    EffectType,
)


class CreateCardEffectSchema(BaseModel):

    action: CardAction
    value: NonNegativeInt
    effect_type: EffectType
    condition_type: ConditionType | None = None
    condition_value: NonNegativeInt | None = None


class CreateCardSchema(BaseModel):

    name: str
    crystals_cost: NonNegativeInt
    description: str
    shield: NonNegativeInt
    champion_health: NonNegativeInt = 0
    card_type: CardType
    faction: CardFaction
    icon: str
    start_card: bool = False
    effects: List[CreateCardEffectSchema]


class CardSchema(CreateCardSchema):

    id: int
