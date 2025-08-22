import enum
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import (
    DateTime,
    Enum,
    String,
    func,
    ForeignKey,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB

from .base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.backend.core.models.user import TelegramUser
    from app.backend.core.models.player_state import PlayerState


class GameStatus(str, enum.Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class Game(Base):
    __tablename__ = "games"

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus), default=GameStatus.WAITING
    )

    player1_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    player2_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    active_player_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    non_active_player_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        )
    player_states: Mapped[List["PlayerState"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )
    invite_token: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=True,
    )
    market_cards: Mapped[list[int]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
        server_default=text("'[]'::jsonb"),
    )
    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    player1: Mapped["TelegramUser"] = relationship(
        "TelegramUser",
        foreign_keys=[player1_id],
    )

    player2: Mapped[Optional["TelegramUser"]] = relationship(
        "TelegramUser",
        foreign_keys=[player2_id],
    )

    active_player: Mapped[Optional["TelegramUser"]] = relationship(
        "TelegramUser",
        foreign_keys=[active_player_id],
    )

    winner: Mapped[Optional["TelegramUser"]] = relationship(
        "TelegramUser",
        foreign_keys=[winner_id],
    )

    def __repr__(self):
        return f"Game id={self.id} status={self.status} player1={self.player1_id} player2={self.player2_id}"
