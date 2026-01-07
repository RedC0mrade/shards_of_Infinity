from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.backend.core.models.play_card_instance import PlayerCardInstance


class DestroyCardCallback(
    CallbackData,
    prefix="destroy_card",
):
    id: int


def destroy_card_keyboard(
    instance_data: list[PlayerCardInstance],
    columns: int = 3,
) -> InlineKeyboardMarkup:

    buttons = []

    for card_instance in instance_data:
        buttons.append(
            InlineKeyboardButton(
                text=card_instance.card.name,
                callback_data=DestroyCardCallback(
                    id=card_instance.id,
                ).pack(),
            )
        )

    keyboard_layout = [
        buttons[i : i + columns] for i in range(0, len(buttons), columns)
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
