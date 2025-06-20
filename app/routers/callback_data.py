from random import randint
from aiogram import Bot, F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ChatAction

from app.keyboards.inline_keyboards import buld_info_kd
from app.keyboards.inline_keyboards import random_num_updated_cb_data

router = Router(name=__name__)

@router.callback_query(F.data == random_num_updated_cb_data)
async def handel_random_site_callback(callback_query: CallbackQuery):
    bot_me = await callback_query.bot.me() # Информация о боте
    # print("Bot_me", bot_me, bot_me.username)
    # await callback_query.bot.answer_callback_query(
    #     callback_query_id=callback_query.id,
    #     url = f"t.me/{bot_me.username}?start={randint(1,100)}" # В команду start передаем случайное число
    # )
    await callback_query.answer(
        url = f"t.me/{bot_me.username}?start={randint(1,100)}" # В команду start передаем случайное число
    )