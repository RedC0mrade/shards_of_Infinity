from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class MoveKBText:
    MARKET = "Рынок"
    HAND = "Рука"
    ATTACK = "Атака Игрока"
    ATTACK_CHAMPION = "Атака чемпиона"
    END = "Конец хода"
    DEFEAT = "Сдаться"


def in_play_card_keyboard():
    market_button = KeyboardButton(text=MoveKBText.MARKET)
    hand_button = KeyboardButton(text=MoveKBText.HAND)
    attack_button = KeyboardButton(text=MoveKBText.ATTACK)
    attack_champion_button = KeyboardButton(text=MoveKBText.ATTACK_CHAMPION)
    end_button = KeyboardButton(text=MoveKBText.END)
    defeat_button = KeyboardButton(text=MoveKBText.DEFEAT)

    button_row = [
        market_button,
        hand_button,
        attack_button,
        attack_champion_button,
        end_button,
        defeat_button,
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=[
            button_row,
        ],
        resize_keyboard=True,
    )
    return markup