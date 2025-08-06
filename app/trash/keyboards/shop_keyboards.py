from enum import IntEnum, auto
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class ShopActions(IntEnum):
    products = auto()
    address = auto()
    root = auto()


class ShopCbData(CallbackData, prefix="shop"):
    actions: ShopActions


class ProductActions(IntEnum):
    details = auto()
    update = auto()
    delete = auto()


class ProductCdData(CallbackData, prefix="product"):
    action: ProductActions
    id: int
    name: str
    price: int


def build_shop_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="show products",
        callback_data=ShopCbData(actions=ShopActions.products).pack(),
    )
    builder.button(
        text="show address",
        callback_data=ShopCbData(actions=ShopActions.address).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def build_products_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Back to root",
        callback_data=ShopCbData(actions=ShopActions.root).pack(),
    )
    for idx, (name, price) in enumerate(
        [
            ("laptop", 1111),
            ("desktop", 2222),
            ("nettop", 3333),
        ],
        start=1,
    ):
        builder.button(
            text=name,
            callback_data=ProductCdData(
                action=ProductActions.details,
                id=idx,
                name=name,
                price=price,
            ),
        )
    builder.adjust(1)
    return builder.as_markup()


def product_details_kb(product_cb_data: ProductCdData) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="back to products",
        callback_data=ShopCbData(actions=ShopActions.products).pack(),
    )
    for lable, action in [
        ("Update", ProductActions.update),
        ("Delete", ProductActions.delete),
    ]:
        builder.button(
            text=lable,
            callback_data=ProductCdData(
                action=action,
                **product_cb_data.model_dump(  # Не явный вариант
                    include={  # передаем те поля, которые хотим включить в ответ
                        "id",
                        "name",
                        "price",
                    }
                ),
                # **product_cb_data.model_dump(exclude={"actions"}), распаковывает модель exclude - исключает поле action
                # id=product_cb_data.id,     явный вариант
                # name=product_cb_data.name,
                # price=product_cb_data.price,
            ),
        )
    builder.adjust(1, 2)
    return builder.as_markup()


def build_update_product_kb(
    product_cb_data: ProductCdData,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Back to product {product_cb_data.name}",
        callback_data=ProductCdData(
            action=ProductActions.details,
            id=product_cb_data.id,
            name=product_cb_data.name,
            price=product_cb_data.price,
        ),
    )
    builder.button(
        text=f"update {product_cb_data.name}",
        callback_data=ProductCdData(
            action=ProductActions.details,
            id=product_cb_data.id,
            name=product_cb_data.name,
            price=product_cb_data.price,
        ),
    )
    return builder.as_markup()
