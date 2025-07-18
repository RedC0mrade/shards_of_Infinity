import enum
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, func, ForeignKey, Integer
from .base_model import Base
from .user import TelegrammUser
from .player_state import PlayerState
from sqlalchemy.orm import Mapped, mapped_column, relationship


class GameStatus(str, enum.Enum):
    WAITING = "waiting"  # Ожидает второго игрока
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class Game(Base):
    __tablename__ = "games"

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus), default=GameStatus.WAITING
    )

    player1_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    turns: Mapped[list["Turn"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )
    current_turn: Mapped[int] = mapped_column(default=1)
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False)
    active_player_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    player_states: Mapped[list["PlayerState"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )


class Turn(Base):
    __tablename__ = "turns"

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    game: Mapped["Game"] = relationship(back_populates="turns")
    active_player_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    turn_number: Mapped[int] = mapped_column(Integer)
