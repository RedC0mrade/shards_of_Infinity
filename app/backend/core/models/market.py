from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer

from .base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.backend.core.models.game import Game
    from app.backend.core.models.card import Card


class MarketSlot(Base):
    __tablename__ = "market_slots"

    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE")
    )
    position: Mapped[int] = mapped_column(Integer)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))

    card: Mapped["Card"] = relationship("Card")
    game: Mapped["Game"] = relationship(
        "Game",
        back_populates="market_slots",
    )
