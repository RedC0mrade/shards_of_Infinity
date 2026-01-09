from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.backend.core.models.play_card_instance import PlayerCardInstance


class AtackChampionCallback(
    CallbackData,
    prefix="champion",
):
    id: int
    champion_health: int


class DestroyChampionCallback(
    CallbackData,
    prefix="destroy_champion",
):
    id: int
    champion_health: int


def attack_champion_keyboard(
    instance_data: list[PlayerCardInstance],
    callback_cls: type[CallbackData],
    columns: int = 3,
) -> InlineKeyboardMarkup:

    buttons = []

    for card_instance in instance_data:
        buttons.append(
            InlineKeyboardButton(
                text=card_instance.card.name,
                callback_data=callback_cls(
                    id=card_instance.id,
                    champion_health=card_instance.card.champion_health,
                ).pack(),
            )
        )

    keyboard_layout = [
        buttons[i : i + columns] for i in range(0, len(buttons), columns)
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
