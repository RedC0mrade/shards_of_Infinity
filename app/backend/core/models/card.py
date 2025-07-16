import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    Enum,
)

from .base_model import Base


class CardFaction(str, enum.Enum):
    WILDS = "Ветвь"
    ORDER = "Орден"
    HOMODEUS = "Хомо Деус"
    DEMIREALM = "Демиреал"
    NEUTRAL = "Нейтральная"


class CardType(str, enum.Enum):
    ALLY = "Союзник"
    CHAMPION = "Чемпион"
    MERCENARY = "Наёмник"
    RELIC = "Реликвия"


class CardAction(str, enum.Enum):
    GET_CARD = "get_card"
    CARD_DESTROY = "card_destroy"
    ATTACK = "attack"
    HEALING = "healing"
    GET_CRYSTAL = "get_crystal"
    CET_MIGHT = "get_might"


class EffectType(str, enum.Enum):
    BASE = "base"
    CONDITIONAL = "conditional"


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = (
        CheckConstraint("cost >= 0", name="cost_non_negative"),
        CheckConstraint("shield >= 0", name="shield_non_negative"),
        CheckConstraint(
            "champion_health >= 0", name="champion_health_non_negative"
        ),
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    cristals_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    shield: Mapped[int] = mapped_column(Integer, nullable=False)
    champion_health: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    faction: Mapped["CardFaction"] = mapped_column(
        Enum(CardFaction),
        default=CardFaction.NEUTRAL,
    )
    icon: Mapped[str] = mapped_column(String(100), nullable=False)
    effects: Mapped[list["CardEffect"]] = relationship(
        back_populates="card", cascade="all, delete-orphan"
    )


class CardEffect(Base):
    __tablename__ = "card_base_effects"
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped[Card] = relationship(back_populates="base_effect")
    action: Mapped["CardAction"] = mapped_column(Enum(CardAction))
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[EffectType] = mapped_column(
        Enum(EffectType), nullable=False
    )
    condition: Mapped[str | None] = mapped_column(String(200), nullable=True)
