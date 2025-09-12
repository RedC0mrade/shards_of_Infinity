from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class MoveKBText:
    MARKET = "Рынок"
    HAND = "Рука"
    ATTACK = "Атака Игрока"
    ATTACK_CHAMPION = "Атака чемпиона"
    GAME_PARAMETERS = "Игравые параметры"
    END = "Конец хода"
    DEFEAT = "Сдаться"
    SHILD = "Щит"


def in_play_card_keyboard():
    market_button = KeyboardButton(text=MoveKBText.MARKET)
    hand_button = KeyboardButton(text=MoveKBText.HAND)
    attack_button = KeyboardButton(text=MoveKBText.ATTACK)
    attack_champion_button = KeyboardButton(text=MoveKBText.ATTACK_CHAMPION)
    end_button = KeyboardButton(text=MoveKBText.END)
    defeat_button = KeyboardButton(text=MoveKBText.DEFEAT)
    parameters_button = KeyboardButton(text=MoveKBText.GAME_PARAMETERS)

    button_row = [
        market_button,
        hand_button,
        attack_button,
        attack_champion_button,
        end_button,
        defeat_button,
        parameters_button,
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=[
            button_row,
        ],
        resize_keyboard=True,
    )
    return markup

def non_play_card_keyboard():
    market_button = KeyboardButton(text=MoveKBText.MARKET)
    hand_button = KeyboardButton(text=MoveKBText.HAND)
    defeat_button = KeyboardButton(text=MoveKBText.DEFEAT)
    shild_button = KeyboardButton(text=MoveKBText.SHILD)
    parameters_button = KeyboardButton(text=MoveKBText.GAME_PARAMETERS)
    button_row = [
        market_button,
        hand_button,
        defeat_button,
        shild_button,
        parameters_button
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=[
            button_row,
        ],
        resize_keyboard=False,
    )
    return markup