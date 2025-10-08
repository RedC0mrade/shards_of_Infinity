from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Enum, Boolean, text

from .base_model import Base
import enum

if TYPE_CHECKING:
    from app.backend.core.models.card import Card
    from app.backend.core.models.game import Game
    from app.backend.core.models.player_state import PlayerState


class CardZone(str, enum.Enum):
    PLAYER_DECK = "player_deck"
    COMMON_DECK = "common_deck"
    HAND = "hand"
    DISCARD = "discard"
    IN_PLAY = "in_play"
    EXILED = "exiled"
    MARKET = "market"
    CHAMPION = "champion"  # если карта активирована
    OTHER = "other"  # на будущее


class PlayerCardInstance(Base):
    __tablename__ = "player_card_instances"

    player_state_id: Mapped[int | None] = mapped_column(
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
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))

    zone: Mapped[CardZone] = mapped_column(Enum(CardZone))
    delete_mercenary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("FALSE"),
    )

    card: Mapped["Card"] = relationship("Card", lazy="selectin")
    game: Mapped["Game"] = relationship("Game")
    player_state: Mapped["PlayerState"] = relationship(
        "PlayerState",
        back_populates="cards",
    )

    def __repr__(self) -> str:
        return (
            f"<PlayerCardInstance id={self.id} "
            f"card_id={self.card_id} "
            f"zone={self.zone}>"
        )
