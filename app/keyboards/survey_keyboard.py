from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def build_yes_or_no_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button = InlineKeyboardButton(
        text="Yes"
    )
    builder.button = InlineKeyboardButton(
        text="No"
    )
    builder.adjust(1)
    return builder.as_markup()