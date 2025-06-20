from aiogram import Bot, F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


router = Router(name=__name__)
@router.message(Command("info", prefix="/!"))
async def handel_info_command(message: types.Message):
    tg_channel_bt = InlineKeyboardButton(
        text="Канал",
        url="https://t.me/+TRzHuBxuIxZlY2Qy"
    )
    pic = InlineKeyboardButton(
        text="Картинка",
        url="https://i.pinimg.com/736x/ac/15/8e/ac158efaaef7f12cbd837dac7ad0f0fe.jpg"
    )
    row = [tg_channel_bt, pic]
    rows = [row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text="Ссылки и прочие ресурсы",
        reply_markup=markup,
    )