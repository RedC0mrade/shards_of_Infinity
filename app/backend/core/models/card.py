from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from .base_model import Base


class Card(Base):
    tablename = "cards"