from pydantic import BaseModel, Field
from typing import Optional
from app.backend.core.models.card import CardFaction, CardType

class CardBase(BaseModel):
    name: str = Field(..., max_length=100)
    cost: int = Field(..., ge=0)
    faction: CardFaction
    card_type: CardType
    damage: int = Field(default=0, ge=0)
    healing: int = Field(default=0, ge=0)
    mastery: int = Field(default=0, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)

class CardCreate(CardBase):
    pass

class CardOut(CardBase):
    id: int
