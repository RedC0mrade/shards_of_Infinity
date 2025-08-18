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
    CARD = "card"
    CARD_DESTROY = "card_destroy"
    ATTACK = "attack"
    HEALING = "healing"
    CRYSTAL = "crystal"
    MIGHT = "might"
    SPECiAL = "special"
    TAKE_MERCENARY = "take_mercenary"
    IMMUNITY = "immunity"
    COPY_EFFECT = "copy_effect"
    DOUBLE_CHOISE = "double_choice"
    NONE = "none"


class EffectType(str, enum.Enum):
    BASE = "base"
    CONDITIONAL = "conditional"


class ConditionType(str, enum.Enum):
    MASTERY = "mastery"
    PLAYER_HEALTH = "player_health"
    ENEMY_HAS_CHAMPION = "enemy_has_champion"
    YOU_HAVE_CARD_IN_RESET = "you_have_card"
    CARD_ON_TABLE = "card_on_table"
    NONE = "none"


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = (
        CheckConstraint(
            "crystals_cost >= 0",
            name="cost_non_negative",
        ),
        CheckConstraint(
            "shield >= 0",
            name="shield_non_negative",
        ),
        CheckConstraint(
            "champion_health >= 0",
            name="champion_health_non_negative",
        ),
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    crystals_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    shield: Mapped[int] = mapped_column(Integer, nullable=False)
    champion_health: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    faction: Mapped["CardFaction"] = mapped_column(
        Enum(CardFaction),
    )
    card_type: Mapped["CardType"] = mapped_column(
        Enum(CardType),
    )
    icon: Mapped[str] = mapped_column(String(100), nullable=False)
    start_card: Mapped[bool] = mapped_column(Boolean, default=False)
    effects: Mapped[list["CardEffect"]] = relationship(
        back_populates="card",
        cascade="all, delete-orphan",
        lazy="joined",
    )


class CardEffect(Base):
    __tablename__ = "card_effects"
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped[Card] = relationship(back_populates="effects")
    action: Mapped["CardAction"] = mapped_column(Enum(CardAction))
    value: Mapped[int] = mapped_column(Integer, nullable=True)
    effect_type: Mapped[EffectType] = mapped_column(
        Enum(EffectType), nullable=False
    )
    condition_type: Mapped[ConditionType | None] = mapped_column(
        Enum(ConditionType),
        nullable=True,
    )
    condition_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
