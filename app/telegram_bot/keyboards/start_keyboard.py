from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

class StartKBText:
    START_GAME = "Start Game"
    ACCEPT_INVITATION = "Accept Invitation"

def start_keyboard():
    start_button = KeyboardButton(text=StartKBText.START_GAME)
    accept_button = KeyboardButton(text=StartKBText.ACCEPT_INVITATION)

    button_row = [
        start_button,
        accept_button,        
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=[
        button_row,
    ],
    resize_keyboard=True
    )
    return markup