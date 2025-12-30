from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, Integer, Boolean, text
from typing import TYPE_CHECKING

from .base_model import Base


if TYPE_CHECKING:
    from app.backend.core.models.play_card_instance import PlayerCardInstance
    from app.backend.core.models.game import Game
    from app.backend.core.models.user import TelegramUser


class PlayerState(Base):
    __tablename__ = "player_states"

    player = relationship("TelegramUser", back_populates="player_states")
    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("games.id", ondelete="CASCADE"),
    )
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    
    health: Mapped[int] = mapped_column(Integer, default=50)
    mastery: Mapped[int] = mapped_column(Integer, default=0)
    crystals: Mapped[int] = mapped_column(Integer, default=0)
    power: Mapped[int] = mapped_column(Integer, default=0)  # Урон (боевые очки)
    shield: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
    )

    wilds_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
    )
    order_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
    )
    homodeus_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
    )
    demirealm_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
    )
    invulnerability: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("FALSE"),
    )
    concentration: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("FALSE"),
    )
    game: Mapped["Game"] = relationship(
        "Game",
        back_populates="player_states",
    )
    cards: Mapped[list["PlayerCardInstance"]] = relationship(
        back_populates="player_state",
        cascade="all, delete-orphan",
    )
