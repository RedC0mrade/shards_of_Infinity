from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Enum, Boolean, text

from app.backend.core.models.card import Card
from app.backend.core.models.player_state import PlayerState
from .base_model import Base
import enum


class CardZone(str, enum.Enum):
    PLAYER_DECK = "player_deck"
    COMMON_DECK = "common_deck"
    HAND = "hand"
    DISCARD = "discard"
    IN_PLAY = "in_play"
    EXILED = "exiled"
    MARKET = "market"  # если потребуется
    CHAMPION = "champion"  # если карта активирована
    OTHER = "other"  # на будущее


class PlayerCardInstance(Base):
    __tablename__ = "player_card_instances"

    player_state_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            "player_states.id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    game_id: Mapped[int] = mapped_column(
        ForeignKey(
            "games.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    card_id: Mapped[int] = mapped_column(
        ForeignKey(
            "cards.id"
        )
    )

    zone: Mapped[CardZone] = mapped_column(Enum(CardZone))
    delete_mercenamy: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("FALSE"),
    )

    card: Mapped["Card"] = relationship("Card", lazy="selectin")
    player_state: Mapped[Optional["PlayerState"]] = relationship(
        "PlayerState",
        back_populates="cards",
    )

    def __repr__(self) -> str:
        return (
            f"<PlayerCardInstance id={self.id} "
            f"card_id={self.card_id} "
            f"zone={self.zone}>"
        )
