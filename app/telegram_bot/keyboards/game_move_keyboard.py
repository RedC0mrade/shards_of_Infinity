from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class MoveKBText:
    MARKET = "Рынок"
    HAND = "Рука"
    CARDS_IN_PLAY = "Сыгранные карты"
    ATTACK = "Атака Игрока"
    ATTACK_CHAMPION = "Атака чемпиона"
    GAME_PARAMETERS = "Игравые параметры ирока"
    ENEMY_PARAMETERS = "Игровые параметры Противника"
    END = "Конец хода"
    DEFEAT = "Сдаться"
    SHILD = "Щит"


def in_play_card_keyboard():
    market_button = KeyboardButton(text=MoveKBText.MARKET)
    hand_button = KeyboardButton(text=MoveKBText.HAND)
    cards_in_play = KeyboardButton(text=MoveKBText.CARDS_IN_PLAY)
    attack_button = KeyboardButton(text=MoveKBText.ATTACK)
    attack_champion_button = KeyboardButton(text=MoveKBText.ATTACK_CHAMPION)
    end_button = KeyboardButton(text=MoveKBText.END)
    defeat_button = KeyboardButton(text=MoveKBText.DEFEAT)
    parameters_button = KeyboardButton(text=MoveKBText.GAME_PARAMETERS)
    enemy_parameters_button = KeyboardButton(text=MoveKBText.ENEMY_PARAMETERS)

    button_row = [
        market_button,
        hand_button,
        cards_in_play,
        attack_button,
        attack_champion_button,
        end_button,
        defeat_button,
    ]
    parameters_row = [
        enemy_parameters_button,
        parameters_button,
    ]
        
    markup = ReplyKeyboardMarkup(
        keyboard=[
            button_row,
            parameters_row,
        ],
    )
    return markup

def non_play_card_keyboard():
    market_button = KeyboardButton(text=MoveKBText.MARKET)
    hand_button = KeyboardButton(text=MoveKBText.HAND)
    cards_in_play = KeyboardButton(text=MoveKBText.CARDS_IN_PLAY)
    defeat_button = KeyboardButton(text=MoveKBText.DEFEAT)
    shild_button = KeyboardButton(text=MoveKBText.SHILD)
    parameters_button = KeyboardButton(text=MoveKBText.GAME_PARAMETERS)
    button_row = [
        market_button,
        hand_button,
        cards_in_play,
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