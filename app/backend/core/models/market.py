from sqlalchemy import ForeignKey, Integer

from app.backend.core.models.card import Card
from .base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MarketSlot(Base):
    __tablename__ = "market_slots"

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    position: Mapped[int] = mapped_column(Integer)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))

    card: Mapped["Card"] = relationship("Card")
