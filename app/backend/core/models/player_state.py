from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Boolean
from typing import TYPE_CHECKING

from .base_model import Base


if TYPE_CHECKING:
    from app.backend.core.models.play_card_instance import PlayerCardInstance
    from app.backend.core.models.game import Game
    from app.backend.core.models.user import TelegrammUser


class PlayerState(Base):
    __tablename__ = "player_states"

    player = relationship("TelegrammUser", back_populates="player_states")
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    health: Mapped[int] = mapped_column(Integer, default=50)  # Стартовое здоровье
    mastery: Mapped[int] = mapped_column(Integer, default=0)  # Уровень мастерства
    crystals: Mapped[int] = mapped_column(Integer, default=0)  # Кристаллы (ресурс)
    power: Mapped[int] = mapped_column(Integer, default=0)  # Урон (боевые очки)

    deck_count: Mapped[int] = mapped_column(Integer, default=0)  # Осталось в колоде
    discard_count: Mapped[int] = mapped_column(Integer, default=0)  # В сбросе
    hand_count: Mapped[int] = mapped_column(Integer, default=0)  # В руке

    is_defeated: Mapped[bool] = mapped_column(Boolean, default=False)

    # relationships
    game: Mapped["Game"] = relationship("Game", back_populates="player_states")
    cards: Mapped[list["PlayerCardInstance"]] = relationship(
        back_populates="player_state", cascade="all, delete-orphan"
    )
