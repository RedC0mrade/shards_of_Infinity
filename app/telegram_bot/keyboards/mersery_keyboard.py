from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.backend.core.models.card import Card
from app.backend.core.models.play_card_instance import PlayerCardInstance


class MercenaryKBText:
    PLAY_CARD = "Разыграть карту сейчас"
    TAKE_CARD = "Отправить в свою колоду"


class MercenaryCallback(CallbackData, prefix="mercenary"):
    card_instance_id: int
    play_now: bool
    player_state_id: int
    game_id: int
    card_id: int


def play_mercenary(
    card_instance_id: int,
    player_state_id: int,
    game_id: int,
    card_id: int,
) -> InlineKeyboardMarkup:

    play_mercenary_button = InlineKeyboardButton(
        text=MercenaryKBText.PLAY_CARD,
        callback_data=MercenaryCallback(
            card_instance_id=card_instance_id,
            play_now=True,
            player_state_id=player_state_id,
            game_id=game_id,
            card_id=card_id,
        ).pack(),
    )
    discard_mercenary_button = InlineKeyboardButton(
        text=MercenaryKBText.TAKE_CARD,
        callback_data=MercenaryCallback(
            card_instance_id=card_instance_id,
            play_now=False,
        ).pack(),
    )
    mercenary_buttons = [play_mercenary_button, discard_mercenary_button]
    markup = InlineKeyboardMarkup(inline_keyboard=mercenary_buttons)
    return markup
