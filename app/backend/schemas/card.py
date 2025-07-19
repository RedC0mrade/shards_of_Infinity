from pydantic import BaseModel, Field
from typing import Annotated, List
from app.backend.core.models.card import CardAction, CardFaction, ConditionType, EffectType

PositiveInt = Annotated[int, Field(ge=0)]

class CreateCardSchema(BaseModel):
    id: int
    name: str
    crystals_cost: PositiveInt
    description: str
    shiel: PositiveInt
    champion_health: PositiveInt
    faction: CardFaction
    icon: str

class CreateCardEffectSchema(BaseModel):
    id: int
    card_id: PositiveInt
    card: CreateCardSchema
    action: CardFaction
    value: PositiveInt
    effect_type: EffectType
    condition_type: ConditionType | None = None
    condition_value: PositiveInt

