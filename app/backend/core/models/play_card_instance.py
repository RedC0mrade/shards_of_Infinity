from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    Enum,
    Boolean,
    UniqueConstraint,
    text,
)

from .base_model import Base, CustomEnum
import enum

if TYPE_CHECKING:
    from app.backend.core.models.card import Card
    from app.backend.core.models.game import Game
    from app.backend.core.models.player_state import PlayerState


class CardZone(str, enum.Enum):
    CHAMPION = "champion"  # ЧЕМПИОНЫ, которые не сбрасываются со стола после конца хода
    COMMON_DECK = "common_deck"  # ОБЩАЯ колода карт
    DISCARD = "discard"  # Карты в СБРОСЕ у игрока
    EXILED = "exiled"  # УДАЛЕННЫЕ карты из игры, наемники или уничтоженные
    HAND = "hand"  # Карты в РУКЕ игрока
    IN_ACTION = "in_action" # Карта сыгранная в данный момент
    # IN_PLAY = "in_play"  # Разыгранная карты 
    MARKET = "market"  # Карты на РЫНКЕ
    ON_BOARD = "on_board" # Карты на столе
    PLAYER_DECK = "player_deck"  # Активные карты В КОЛОДЕ игрока


class PlayerCardInstance(Base):
    __tablename__ = "player_card_instances"
    __table_args__ = (
        CheckConstraint(
            "(zone != 'market') OR (position_on_market IS NOT NULL)",
            name="market_position_required",
        ),
        CheckConstraint(
            "(zone = 'market') OR (position_on_market IS NULL)",
            name="position_only_for_market",
        ),
        UniqueConstraint(  # Добавляем уникальность для game_id и card_id
            "game_id", "card_id", name="uq_game_card"
        ),
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
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), unique=True)

    zone: Mapped[CardZone] = mapped_column(
        CustomEnum(CardZone, name="cardzone")
    )
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
    invulnerability: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("FALSE"),
    )
    card: Mapped["Card"] = relationship("Card", lazy="joined")
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
