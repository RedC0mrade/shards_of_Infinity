from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class MoveKBText:
    MARKET = "Рынок"
    HAND = "Рука"
    PLAYER_DISCARD = "Карты в сбросе игрока"
    CARDS_IN_PLAY = "Сыгранные карты"
    ATTACK = "Атака Игрока"
    ATTACK_CHAMPION = "Атака чемпиона"
    GAME_PARAMETERS = "Игравые параметры ирока"
    ENEMY_PARAMETERS = "Игровые параметры Противника"
    END = "Конец хода"
    DEFEAT = "Сдаться"
    SHILD = "Щит"
    CHAMPION_PLAY = "Разыграть свойства чемптонов"


def in_play_card_keyboard():
    """Клавиату для общеигрового меню, активного игрока"""
    market_button = KeyboardButton(text=MoveKBText.MARKET)
    hand_button = KeyboardButton(text=MoveKBText.HAND)
    cards_in_play = KeyboardButton(text=MoveKBText.CARDS_IN_PLAY)
    attack_button = KeyboardButton(text=MoveKBText.ATTACK)
    attack_champion_button = KeyboardButton(text=MoveKBText.ATTACK_CHAMPION)
    end_button = KeyboardButton(text=MoveKBText.END)
    defeat_button = KeyboardButton(text=MoveKBText.DEFEAT)
    parameters_button = KeyboardButton(text=MoveKBText.GAME_PARAMETERS)
    enemy_parameters_button = KeyboardButton(text=MoveKBText.ENEMY_PARAMETERS)
    player_discard_button = KeyboardButton(text=MoveKBText.PLAYER_DISCARD)
    champion_play_button = KeyboardButton(text=MoveKBText.CHAMPION_PLAY)

    button_row = [
        attack_button,
        attack_champion_button,
        end_button,
        defeat_button,
    ]

    cards_row = [
        market_button,
        hand_button,
        player_discard_button,
        cards_in_play,
        champion_play_button,
    ]

    parameters_row = [
        enemy_parameters_button,
        parameters_button,
    ]

    markup = ReplyKeyboardMarkup(
        keyboard=[
            cards_row,
            button_row,
            parameters_row,
        ],
    )
    return markup


def non_play_card_keyboard():
    """Клавиатура общеигравого меню, для игрока ждущего своего хода."""
    
    market_button = KeyboardButton(text=MoveKBText.MARKET)
    hand_button = KeyboardButton(text=MoveKBText.HAND)
    cards_in_play = KeyboardButton(text=MoveKBText.CARDS_IN_PLAY)
    defeat_button = KeyboardButton(text=MoveKBText.DEFEAT)
    shild_button = KeyboardButton(text=MoveKBText.SHILD)
    parameters_button = KeyboardButton(text=MoveKBText.GAME_PARAMETERS)
    enemy_parameters_button = KeyboardButton(text=MoveKBText.ENEMY_PARAMETERS)
    button_row = [
        defeat_button,
        shild_button,
        parameters_button,
        enemy_parameters_button,
    ]
    button_row_1 = [
        market_button,
        hand_button,
        cards_in_play,
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=[
            button_row_1,
            button_row,
        ],
        resize_keyboard=False,
    )
    return markup
