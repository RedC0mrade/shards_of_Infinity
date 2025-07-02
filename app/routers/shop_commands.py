from aiogram import F, Router
from aiogram.filters import Command
from aiogram import types

from app.keyboards.shop_keyboards import ShopCbData, build_shop_kb

router = Router(name=__name__)

@router.message(Command("shop", prefix="/!"))
async def send_shop_message_kb(message: types.Message):
    await message.answer(
        text = "your shop actions:",
        reply_markup=build_shop_kb()
    )
