from pydantic import BaseModel, Field
from typing import Annotated, List
from app.backend.core.models.card import (
    CardAction,
    CardFaction,
    CardType,
    ConditionType,
    EffectType,
)

PositiveInt = Annotated[int, Field(ge=0)]


class CreateCardEffectSchema(BaseModel):

    action: CardAction
    value: PositiveInt
    effect_type: EffectType
    condition_type: ConditionType | None = None
    condition_value: PositiveInt | None = None


class CreateCardSchema(BaseModel):

    name: str
    crystals_cost: PositiveInt
    description: str
    shield: PositiveInt
    champion_health: PositiveInt = 0
    card_type: CardType
    faction: CardFaction
    icon: str
    effects: List[CreateCardEffectSchema]


class CardSchema(CreateCardSchema):

    id: int
