from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import TYPE_CHECKING

from .base_model import Base


if TYPE_CHECKING:
    from app.backend.core.models.player_state import PlayerState


class TelegrammUser(Base):
    __tablename__ = "users"

    telegramm_id: Mapped[int] = mapped_column(Integer, unique=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=True)
    last_name: Mapped[str] = mapped_column(String(20), nullable=True)
    player_states: Mapped["PlayerState"] = relationship(
        "PlayerState",
        back_populates="player",
    )
