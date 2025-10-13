from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Enum, Boolean, UniqueConstraint, text

from .base_model import Base
import enum

if TYPE_CHECKING:
    from app.backend.core.models.card import Card
    from app.backend.core.models.game import Game
    from app.backend.core.models.player_state import PlayerState


class CardZone(str, enum.Enum):
    PLAYER_DECK = "player_deck" # Активные карты В КОЛОДЕ игрока
    COMMON_DECK = "common_deck" # ОБЩАЯ колода карт
    HAND = "hand"               # Карты в РУКЕ игрока
    DISCARD = "discard"         # Карты в СБРОСЕ у игрока
    IN_PLAY = "in_play"         # Карты которые на СТОЛЕ
    EXILED = "exiled"           # УДАЛЕННЫЕ карты из игры, наемники или уничтоженные
    MARKET = "market"           # Карты на РЫНКЕ
    CHAMPION = "champion"       # ЧЕМПИОНЫ, которые не сбрасываются со стола после конца хода
    OTHER = "other"             # на будущее


class PlayerCardInstance(Base):
    __tablename__ = "player_card_instances"
    __table_args__ = (
        CheckConstraint(
            "(zone != 'MARKET') OR (position_on_market IS NOT NULL)",
            name="market_position_required"
        ),
        CheckConstraint(
            "(zone = 'MARKET') OR (position_on_market IS NULL)",
            name="position_only_for_market"
        ),
        UniqueConstraint(  # Добавляем уникальность для game_id и card_id
            "game_id", 
            "card_id", 
            name="uq_game_card"
        )
    )

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
    position_on_market: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        server_default=text("NULL"),
        nullable=True,
    )
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
