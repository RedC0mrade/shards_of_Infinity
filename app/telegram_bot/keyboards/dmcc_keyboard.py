from enum import Enum
from collections.abc import Callable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.backend.core.models.play_card_instance import PlayerCardInstance


class CardButtonText(Enum):
    CARD_NAME = "card_name"
    PLAY_NOW = "play_now"
    TAKE_TO_DECK = "take_to_deck"
    # TAKE_TO_HAND = "take_to_hand"

    def resolve(self, card_instance: PlayerCardInstance) -> str:
        if self is CardButtonText.CARD_NAME:
            return card_instance.card.name

        if self is CardButtonText.PLAY_NOW:
            return "🎲 Разыграть карту сейчас"

        if self is CardButtonText.TAKE_TO_DECK:
            return "📥 Отправить в колоду"

        # if self is CardButtonText.TAKE_TO_DECK:
        #     return "✋ Отправить в руку"

        raise ValueError(f"Unknown CardButtonText: {self}")


class CardCallback(CallbackData, prefix="card"):
    id: int


class MarketCallback(CallbackData, prefix="market"):
    id: int


class AttackChampionCallback(CallbackData, prefix="champion"):
    id: int


class DestroyChampionCallback(CallbackData, prefix="destroy_champion"):
    id: int


class DestroyCardCallback(CallbackData, prefix="destroy_card"):
    id: int


class TakeMercenaryCallback(CallbackData, prefix="take_mercenary"):
    id: int


class TakeChampionyCallback(CallbackData, prefix="take_champion"):
    id: int


class ChooseCardCallback(CallbackData, prefix="choose_card"):
    id: int


class MercenaryCallback(CallbackData, prefix="mercenary"):
    id: int
    play_now: bool


class KeyboardFactory:
    """
    Фабрика inline-клавиатур для карточной игры
    """

    @staticmethod
    def _build_grid(
        buttons: list[InlineKeyboardButton],
        columns: int,
    ) -> list[list[InlineKeyboardButton]]:
        return [
            buttons[i : i + columns] for i in range(0, len(buttons), columns)
        ]

    @classmethod
    def cards(
        cls,
        instance_data: list[PlayerCardInstance],
        callback_factory: Callable[[PlayerCardInstance], CallbackData],
        text_type: CardButtonText = CardButtonText.CARD_NAME,
        columns: int = 3,
    ) -> InlineKeyboardMarkup:
        """
        Универсальная клавиатура для списка карт
        """

        buttons = [
            InlineKeyboardButton(
                text=text_type.resolve(card_instance),
                callback_data=callback_factory(card_instance).pack(),
            )
            for card_instance in instance_data
        ]

        return InlineKeyboardMarkup(
            inline_keyboard=cls._build_grid(buttons, columns)
        )

    # ---------- Конкретные фабрики ----------

    @classmethod
    def market(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: MarketCallback(id=c.id),
        )

    @classmethod
    def play_card(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: CardCallback(id=c.id),
        )

    @classmethod
    def attack_champion(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: AttackChampionCallback(id=c.id),
        )

    @classmethod
    def destroy_champion(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: DestroyChampionCallback(id=c.id),
        )

    @classmethod
    def take_champion(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: TakeChampionyCallback(id=c.id),
        )

    @classmethod
    def choose_card(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: ChooseCardCallback(id=c.id),
        )

    @classmethod
    def take_mercenary(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: TakeMercenaryCallback(id=c.id),
        )

    @classmethod
    def destroy_card(
        cls,
        instance_data: list[PlayerCardInstance],
    ) -> InlineKeyboardMarkup:
        return cls.cards(
            instance_data=instance_data,
            callback_factory=lambda c: DestroyCardCallback(id=c.id),
        )

    # ---------- Mercenary ----------

    @staticmethod
    def mercenary(
        card_instance_id: int,
    ) -> InlineKeyboardMarkup:

        play_button = InlineKeyboardButton(
            text=CardButtonText.PLAY_NOW.resolve(None),
            callback_data=MercenaryCallback(
                id=card_instance_id,
                play_now=True,
            ).pack(),
        )

        take_button = InlineKeyboardButton(
            text=CardButtonText.TAKE_TO_DECK.resolve(None),
            callback_data=MercenaryCallback(
                id=card_instance_id,
                play_now=False,
            ).pack(),
        )

        return InlineKeyboardMarkup(
            inline_keyboard=[[play_button, take_button]]
        )
