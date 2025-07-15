import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, CheckConstraint, Integer, String, Enum

from .base_model import Base


class CardFaction(str, enum.Enum):
    WILDS = "Ветвь"
    ORDER = "Орден"
    HOMODEUS = "Хомо Деус"
    DEMIREALM = "Демиреал"
    NEUTRAL = "Нейтральная"


class CardType(str, enum.Enum):
    CHAMPION = "Чемпион"
    MERCENARY = "Наёмник"
    SPELL = "Заклинание"


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = (
        CheckConstraint("cost >= 0", name="cost_non_negative"),
        CheckConstraint("damage >= 0", name="damage_non_negative"),
        CheckConstraint("healing >= 0", name="healing_non_negative"),
        CheckConstraint("mastery >= 0", name="mastery_non_negative"),
        CheckConstraint("shield >= 0", name="shield_non_negative"),
    )
    name = Mapped[str] = mapped_column(String(20), nullable=False)
    cost = Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    shield: Mapped[int] = mapped_column(Integer, nullable=False)
    faction = Mapped[CardFaction] = mapped_column(
        Enum(CardFaction),
        default=CardFaction.NEUTRAL,
    )
    damage: Mapped[int] = mapped_column(Integer, default=0)
    healing: Mapped[int] = mapped_column(Integer, default=0)