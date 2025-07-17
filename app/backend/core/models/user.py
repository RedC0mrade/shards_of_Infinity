from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from .base_model import Base


class TelegrammUser(Base):
    __tablename__ = "users"

    telegramm_id: Mapped[int] = mapped_column(Integer, unique=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=True)
    last_name: Mapped[str] = mapped_column(String(20), nullable=True)
