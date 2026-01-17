from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.backend.core.models.play_card_instance import PlayerCardInstance


class CardCallback(
    CallbackData,
    prefix="card",
):
    id: int
    name: str


class MarketCallback(
    CallbackData,
    prefix="market",
):
    id: int
    name: str


def make_card_move_keyboard(
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
                    id=card_instance.card.id,
                    name=card_instance.card.name,
                ).pack(),
            )
        )

    keyboard_layout = [
        buttons[i : i + columns] for i in range(0, len(buttons), columns)
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
