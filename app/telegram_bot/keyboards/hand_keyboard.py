from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.backend.core.models.play_card_instance import PlayerCardInstance


def make_card_move_keyboard(cards_data: list[PlayerCardInstance]) -> InlineKeyboardMarkup:
    card_btns = []
    for data in cards_data:
        button = InlineKeyboardButton(
            text = data.card.name,
            callback_data=f"play_card:{data.id}"
        )
        card_btns.append(button)
    markup = InlineKeyboardMarkup(inline_keyboard=[card_btns])
    return markup