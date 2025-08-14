from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Integer, String
from typing import TYPE_CHECKING


from .base_model import Base


if TYPE_CHECKING:
    from app.backend.core.models.player_state import PlayerState


class TelegramUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,  # Делаем PK
        autoincrement=False  # Отключаем автоинкремент
    )
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(20), nullable=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=True)
    last_name: Mapped[str] = mapped_column(String(20), nullable=True)
    player_states: Mapped["PlayerState"] = relationship(
        "PlayerState",
        back_populates="player",
    )
    victories: Mapped[int] = mapped_column(Integer, default=0)
    defeats: Mapped[int] = mapped_column(Integer, default=0)

    def __init__(self, chat_id: int, **kwargs):
            super().__init__(chat_id=chat_id, id=chat_id, **kwargs)