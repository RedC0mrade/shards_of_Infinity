from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder



def build_yes_or_no_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="Yes"
    )
    builder.button(
        text="No"
    )
    builder.adjust(1)
    return builder.as_markup()