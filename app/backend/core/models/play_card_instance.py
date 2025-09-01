from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Enum, Boolean

from app.backend.core.models.card import Card
from app.backend.core.models.player_state import PlayerState
from .base_model import Base
import enum


class CardZone(str, enum.Enum):
    DECK = "deck"
    HAND = "hand"
    DISCARD = "discard"
    IN_PLAY = "in_play"
    EXILED = "exiled"
    MARKET = "market"  # если потребуется
    CHAMPION = "champion"  # если карта активирована
    OTHER = "other"  # на будущее


class PlayerCardInstance(Base):
    __tablename__ = "player_card_instances"

    id: Mapped[int] = mapped_column(primary_key=True)

    player_state_id: Mapped[int] = mapped_column(
        ForeignKey(
            "player_states.id",
            ondelete="CASCADE",
        )
    )
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))

    zone: Mapped[CardZone] = mapped_column(Enum(CardZone))
    # order_in_zone: Mapped[int] = mapped_column(Integer, default=0)

    # is_exhausted: Mapped[bool] = mapped_column(Boolean, default=False)
    # was_played_this_turn: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    card: Mapped["Card"] = relationship("Card")
    player_state: Mapped["PlayerState"] = relationship(
        "PlayerState",
        back_populates="cards",
    )
