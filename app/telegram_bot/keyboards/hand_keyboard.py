from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.backend.core.models.play_card_instance import PlayerCardInstance


class CallBackCard(
    CallbackData,
    prefix="card",
):
    id: int
    name: str


def make_card_move_keyboard(
    instance_data: list[PlayerCardInstance],
) -> InlineKeyboardMarkup:
    card_btns = []
    for card_instance in instance_data:
        button = InlineKeyboardButton(
            text=card_instance.card.name,
            callback_data=CallBackCard(
                id=card_instance.card.id,
                name=card_instance.card.name,
                ).pack(),
        )
        card_btns.append(button)
    markup = InlineKeyboardMarkup(inline_keyboard=[card_btns])
    return markup
