from random import randint
from aiogram import Bot, F, Router, types
from aiogram.types import (
    CallbackQuery,
)

from app.keyboards.actions_keyboards import (
    actions_kb_bulder,
    random_int_3,
    RandomNumCbData,
)
from app.keyboards.inline_keyboards import InlineButtonText


router = Router(name=__name__)


@router.callback_query(RandomNumCbData.filter(F.number % 2 == 0))
async def handle_random_callback_data(
    callback_query: CallbackQuery,
    callback_data: RandomNumCbData,
):
    await callback_query.answer(
        text=f"Четное число {callback_data.number}",
        show_alert=True,
    )


@router.callback_query(RandomNumCbData.filter())
async def handle_random_callback_data(
    callback_query: CallbackQuery,
    callback_data: RandomNumCbData,
):
    await callback_query.answer(
        text=(
            f"Your randon number {callback_data.number}\n"
            f"Callback_data {callback_data}\n"
            f"Callback_data wt !r {callback_data!r}"
        ),
        show_alert=True,
    )


@router.callback_query(F.data == InlineButtonText.random_num_start)
async def handel_random_site_callback(callback_query: CallbackQuery):
    bot_me = await callback_query.bot.me()  # Информация о боте
    await callback_query.answer(
        url=f"t.me/{bot_me.username}?start={randint(1,100)}",  # В команду start передаем случайное число
    )


@router.callback_query(F.data == InlineButtonText.random_num_updated_cb_data)
async def handel_random_site_callback(callback_query: CallbackQuery):
    bot_me = await callback_query.bot.me()  # Информация о боте
    await callback_query.bot.answer_callback_query(
        callback_query_id=callback_query.id,
        url=f"t.me/{bot_me.username}?start={randint(1,100)}",  # В команду start передаем случайное число
    )


@router.callback_query(F.data == InlineButtonText.random_num_start_desctop)
async def handel_random_start_desktop(callback_query: CallbackQuery):
    bot_me = await callback_query.bot.me()
    random = randint(1, 100)
    url = f"https://t.me/{bot_me.username}?start={random}"
    await callback_query.message.answer(
        f"Вот ваша <a href='{url}'>ссылка:</a>, что бы начать!",  # В команду start передаем случайное число для декстопной версии
    )


@router.callback_query(F.data == InlineButtonText.random_int)
async def handel_randon_ineger(callback_query: CallbackQuery):
    random_integer = randint(1, 100)
    await callback_query.answer(  # Внимание такой способ передает не сообщение, а всплывающее окно
        text=f"Ваше случайное число рано {random_integer} cache_time=5",
        cache_time=5,  # Кэшируем ответ на 5 секунд от слишком частого нажатия
    )


@router.callback_query(F.data == InlineButtonText.random_int_1)
async def handel_randon_ineger_1(callback_query: CallbackQuery):
    random_integer = randint(1, 100)
    await callback_query.message.answer(  # Внимание такой способ передает сообщение в чат
        text=f"Ваше случайное число рано {random_integer}",
    )


@router.callback_query(F.data == InlineButtonText.random_int_2)
async def handel_randon_ineger_2(callback_query: CallbackQuery):
    random_integer = randint(1, 100)
    await callback_query.answer(
        text=f"Ваше случайное число рано {random_integer} show_alert=True",
        show_alert=True,  # Выводит окно с кнопкой ok
    )


@router.callback_query(F.data == random_int_3)
async def handel_randon_ineger_3(callback_query: CallbackQuery):
    """Получается динамическая кнопка"""
    random_integer = randint(1, 100)
    await callback_query.answer()  # отмечаем, что кнопка обработана, хотя ничего не происходит
    await callback_query.message.edit_text(  # Изменяем кнопку
        text=f"edit_text {random_integer}",  # Текст сообщения над новой кнопки
        reply_markup=actions_kb_bulder(
            "New random int_3"
        ),  # Передаем параметр в обработчик кнопки
    )
