from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from app.keyboards.shop_keyboards import (
    ShopCbData,
    ShopActions,
    ProductCdData,
    ProductActions,
    build_products_kb,
    build_shop_kb,
    product_details_kb,
)


router = Router(name=__name__)


@router.callback_query(ShopCbData.filter(F.actions == ShopActions.root))
async def handel_root_button(callback_quere: CallbackQuery):
    await callback_quere.answer()
    await callback_quere.message.edit_text(  # Что бы изменить текст, клавиатуру используем edit_text
        text="Your shop actions",
        reply_markup=build_shop_kb(),  # По нажатию кнопки Возвращаем на другую клавиатуру
    )


@router.callback_query(ShopCbData.filter(F.actions == ShopActions.address))
async def handel_my_adress_button(callback_quere: CallbackQuery):
    await callback_quere.answer(
        text="Your address section is still in progress...",
        cache_time=30,
    )


@router.callback_query(ShopCbData.filter(F.actions == ShopActions.products))
async def send_product_list(callback_quere: CallbackQuery):
    await callback_quere.answer()
    await callback_quere.message.edit_text(
        text="Avalible products:",
        reply_markup=build_products_kb(),
    )


@router.callback_query(ProductCdData.filter(F.action == ProductActions.details))
async def handel_product_details_button(
    callback_quere: CallbackQuery,
    callback_data: ProductCdData,
):
    await callback_quere.answer()
    message_text = markdown.text(
        markdown.hbold(f"Product #{callback_data.id}"),
        markdown.text(markdown.hbold("Title:"), callback_data.name),
        markdown.text(markdown.hbold("Price:"), callback_data.price),
        sep="\n",
    )
    await callback_quere.message.edit_text(
        text=message_text,
        reply_markup=product_details_kb(callback_data),
    )
