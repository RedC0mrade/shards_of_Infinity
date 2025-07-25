from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Boolean
from .base_model import Base
from .play_card_instance import PlayerCardInstance


class PlayerState(Base):
    __tablename__ = "player_states"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    health: Mapped[int] = mapped_column(Integer, default=50)        # Стартовое здоровье
    mastery: Mapped[int] = mapped_column(Integer, default=0)        # Уровень мастерства
    crystals: Mapped[int] = mapped_column(Integer, default=0)       # Кристаллы (ресурс)
    power: Mapped[int] = mapped_column(Integer, default=0)          # Урон (боевые очки)

    deck_count: Mapped[int] = mapped_column(Integer, default=0)     # Осталось в колоде
    discard_count: Mapped[int] = mapped_column(Integer, default=0)  # В сбросе
    hand_count: Mapped[int] = mapped_column(Integer, default=0)     # В руке

    is_defeated: Mapped[bool] = mapped_column(Boolean, default=False)

    # relationships
    game = relationship("Game", back_populates="player_states")
    cards: Mapped[list["PlayerCardInstance"]] = relationship(
        back_populates="player_state",
        cascade="all, delete-orphan"
    )
