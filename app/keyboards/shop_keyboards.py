from enum import Enum, auto
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class ShopActions(Enum):
    products = auto()
    address = auto()

class ShopCbData(CallbackData, prefix="shop"):
    actions: ShopActions



def build_shop_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="show products",
        callback_data=ShopCbData(actions=ShopActions.products).pack()
    )
    builder.button(
        text="show address",
        callback_data=ShopCbData(actions=ShopActions.address).pack()
    )
    builder.adjust(1)
    return builder.as_markup()