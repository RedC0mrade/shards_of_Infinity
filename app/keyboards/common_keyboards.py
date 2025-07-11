from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class ButtonText:
    HELLO = "Hellow!"
    START = "Start"
    BYE = "Bye"


def start_keyboard():
    button = KeyboardButton(text=ButtonText.HELLO)
    button_start = KeyboardButton(text=ButtonText.START)
    button_bye = KeyboardButton(text=ButtonText.BYE)
    button_2 = KeyboardButton(text=ButtonText.HELLO + "_2")
    button_start_2 = KeyboardButton(text=ButtonText.START + "_2")
    button_3 = KeyboardButton(text=ButtonText.HELLO + "_3")
    button_start_3 = KeyboardButton(text=ButtonText.START + "_3")

    buttons_row = [button, button_start, button_bye]
    buttons_row_2 = [button_2, button_start_2]
    buttons_row_3 = [button_3, button_start_3]
    markup = ReplyKeyboardMarkup(
        keyboard=[
            buttons_row,
            buttons_row_2,
            buttons_row_3,
        ],
        resize_keyboard=True, # делает кнопки размером с клавиатуру
        one_time_keyboard=True,  # Отвечает за сокрытие кнопок после первого нажатия, но оставляет кнопки активными
    )
    return markup


def get_on_help_kb() -> ReplyKeyboardMarkup:
    numbers = [
        "Card #1️",
        "Card #2️",
        "Card #3️",
        "Card #4️",
        "Card #5️",
        "Card #6️",
    ]
    # buttons_row = [KeyboardButton(text=num) for num in numbers]
    builder = ReplyKeyboardBuilder()
    for num in numbers:
        # builder.button(text=num)
        builder.add(KeyboardButton(text=num))
    builder.adjust(1, 2, 3) # Количество кнопок в ряду
    # builder.row(buttons_row[3], buttons_row[1]) # Добавляет в конец 2 кнопки
    # builder.add(buttons_row[-1]) # Добавляет в конец ещё 1 кнопку
    return builder.as_markup(resize_keyboard=False)
