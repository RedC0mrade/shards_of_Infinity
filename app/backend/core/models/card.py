from __future__ import annotations
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
    WILDS = "wilds"
    ORDER = "order"
    HOMODEUS = "homodeus"
    DEMIREALM = "demirealm"
    NEUTRAL = "neutral"


class CardType(str, enum.Enum):
    ALLY = "ally"
    CHAMPION = "champion"
    MERCENARY = "mercenary"
    RELIC = "relic"


class CardAction(str, enum.Enum):
    TAKE_CARD = "take_card"
    CARD = "card"
    CARD_DESTROY = "card_destroy"
    CHAMPION_DESTROY = "champion_destroy"
    ATTACK = "attack"
    HEALING = "healing"
    CRYSTAL = "crystal"
    MIGHT = "might"
    SPECIAL = "special"
    TAKE_MERCENARY = "take_mercenary"
    IMMUNITY = "immunity"
    COPY_EFFECT = "copy_effect"
    DOUBLE_CHOICE = "double_choice"
    NONE = "none"


class EffectType(str, enum.Enum):
    BASE = "base"
    CONDITIONAL = "conditional"


class ConditionType(str, enum.Enum):
    MASTERY = "mastery"
    PLAYER_HEALTH = "player_health"
    ENEMY_HAS_CHAMPION = "enemy_has_champion"
    YOU_HAVE_CARD_IN_RESET = "you_have_card_in_reset"
    CARD_ON_TABLE = "card_on_table"
    WILDS_ON_TABLE = "wilds_on_table"
    ORDER_ON_TABLE = "order_on_table"
    HOMODEUS_ON_TABLE = "homodeus_on_table"
    DEMIREALM_ON_TABLE = "demirealm_on_table"
    NONE = "none"


class StartCardPlayer(str, enum.Enum):
    FIRST_PLAYER = "first_player"
    SECOND_PLAYER = "second_player"
    OTHER = "other"


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
    shield: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    champion_health: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    faction: Mapped[CardFaction] = mapped_column(
        Enum(CardFaction),
        nullable=False,
    )
    card_type: Mapped[CardType] = mapped_column(
        Enum(CardType),
        nullable=False,
    )
    icon: Mapped[str] = mapped_column(String(100), nullable=False)
    start_card: Mapped[StartCardPlayer] = mapped_column(
        Enum(StartCardPlayer),
        nullable=False,
        default=StartCardPlayer.OTHER,
    )
    effects: Mapped[list["CardEffect"]] = relationship(
        back_populates="card",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Card(id={self.id}), " f"name={self.name}"


class CardEffect(Base):
    __tablename__ = "card_effects"
    card_id: Mapped[int] = mapped_column(
        ForeignKey(
            "cards.id",
            ondelete="CASCADE",
        )
    )
    card: Mapped[Card] = relationship(back_populates="effects")
    action: Mapped["CardAction"] = mapped_column(Enum(CardAction))
    value: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    effect_type: Mapped[EffectType] = mapped_column(
        Enum(EffectType),
        nullable=False,
    )
    condition_type: Mapped[ConditionType | None] = mapped_column(
        Enum(ConditionType),
        nullable=True,
    )
    condition_value: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
