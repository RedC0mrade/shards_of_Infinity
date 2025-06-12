from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ButtonText:
    HELLO = "Hellow!"
    START = "Start"


def start_keyboard():
    button = KeyboardButton(text=ButtonText.HELLO)
    button_start = KeyboardButton(text=ButtonText.START)
    button_2 = KeyboardButton(text=ButtonText.HELLO + "_2")
    button_start_2 = KeyboardButton(text=ButtonText.START + "_2")
    button_3 = KeyboardButton(text=ButtonText.HELLO + "_3")
    button_start_3 = KeyboardButton(text=ButtonText.START + "_3")
    

    buttons_row = [button, button_start]
    buttons_row_2 = [button_2, button_start_2]
    markup = ReplyKeyboardMarkup(
        keyboard=[
            buttons_row,
            buttons_row_2,
        ],
        resize_keyboard=True,
    )
    return markup
