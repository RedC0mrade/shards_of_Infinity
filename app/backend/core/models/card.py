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
    # CARD = "card"
    CARD_DESTROY = "card_destroy"
    CHOOSE_CARD_FROM_MARKET = "choose_card_from_market" # идет в колоду сброса
    TAKE_CARD_FROM_MARKET = "take_card_from_market"     # идет в руку
    CHAMPION_DESTROY = "champion_destroy"
    ATTACK = "attack"
    HEALING = "healing"
    CRYSTAL = "crystal"
    INVULNERABILITY = "invulnerability"
    MIGHT = "might"
    SPECIAL = "special" # Для инквизитора двнных 83 карта
    TAKE_MERCENARY_FROM_RESET = "take_mercenary_from_reset"
    # IMMUNITY = "immunity"
    COPY_EFFECT = "copy_effect"
    DOUBLE_CHOICE = "double_choice"
    NONE = "none"
    DOUBLE_DAMAGE = "double_damage"
    TAKE_DEMIREALM_CARD = "take_demirealm_card"
    ALL_FRACTIONS = "all_fractions"
    ALL_FRACTIONS_IN_HAND = "all_fractions_in_hand" # для карты 86

class EffectType(str, enum.Enum):
    BASE = "base"
    CONDITIONAL = "conditional"


class ConditionType(str, enum.Enum):
    MASTERY = "mastery"
    PLAYER_HEALTH = "player_health"
    ENEMY_HAS_CHAMPION = "enemy_has_champion"
    DEMIREALM_IN_RESET = "demirealm_in_reset"
    CARD_ON_TABLE = "card_on_table"
    WILDS_ON_TABLE = "wilds_on_table"
    ORDER_ON_TABLE = "order_on_table"
    HOMODEUS_ON_TABLE = "homodeus_on_table"
    WILDS_HOMODEUS_DEMIREALM_ON_TABLE = "wilds_homodeus_demirealm_on_table"
    DEMIREALM_ON_TABLE = "demirealm_on_table"
    PLUS_TWO_FOR_EACH_WILDS_IN_PLAY = "plus_two_for_each_wilds_in_play"
    PLUS_TWO_FOR_EACH_DEMIREALM_IN_RESET = (
        "plus_two_for_each_demirealm_in_reset"
    )

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
