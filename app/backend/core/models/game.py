import enum
from datetime import datetime
from sqlalchemy import DateTime, Enum, func, ForeignKey, Integer
from .base_model import Base
from .user import TelegrammUser
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

    player_one_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    player_two_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    player_one: Mapped["TelegrammUser"] = relationship(
        foreign_keys=[player_one_id]
    )
    player_two: Mapped["TelegrammUser"] = relationship(
        foreign_keys=[player_two_id]
    )

    turns: Mapped[list["Turn"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )


class Turn(Base):
    __tablename__ = "turns"

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    game: Mapped["Game"] = relationship(back_populates="turns")

    number: Mapped[int] = mapped_column(Integer)
    active_player_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
