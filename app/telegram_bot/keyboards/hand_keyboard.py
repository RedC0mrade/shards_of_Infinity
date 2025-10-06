from enum import Enum
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
    market: bool = False,
) -> InlineKeyboardMarkup:
    card_buttons = []
    """Клавиатура отвечает за отображение клавиатуры
        выбора карт. Флаг market указывает это карта с руки или с рынка."""
    
    callback_class = MarketCallback if market else CardCallback

    for card_instance in instance_data:
        button = InlineKeyboardButton(
            text=card_instance.card.name,
            callback_data=callback_class(
                id=card_instance.card.id,
                name=card_instance.card.name,
            ).pack(),
        )
        card_buttons.append(button)

    keyboard_layout = [card_buttons[i:i+3] for i in range(0, len(card_buttons), 3)]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
    return markup
