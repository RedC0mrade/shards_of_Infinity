from random import randint
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

random_int_3 = "random_int_3"


class RandomNumCbData(CallbackData, prefix="fixed"):
    number: int


def actions_kb_bulder(
    random_number_text="Rundom number_3",
) -> InlineKeyboardMarkup:
    bulder = InlineKeyboardBuilder()
    bulder.button(
        text=random_number_text,
        callback_data=random_int_3,
    )
    cb_data_1 = RandomNumCbData(number=randint(1, 100))
    bulder.button(
        text=f"Random Number: {cb_data_1.number}",
        callback_data=cb_data_1.pack(),
    )
    cb_data_1 = RandomNumCbData(number=randint(1, 100))
    bulder.button(
        text=f"Random Number: Hidden",
        callback_data=RandomNumCbData(number=randint(1, 100)).pack(),
    )
    bulder.adjust(1)
    return bulder.as_markup()
