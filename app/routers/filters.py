import asyncio
import csv
import io
import logging
import aiohttp
from re import Match

from aiogram.utils.chat_action import ChatActionSender
from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction, ParseMode
from magic_filter import RegexpMode


router = Router()


@router.message(
    F.text.lower().regexp(
        r"too",
        mode=RegexpMode.SEARCH,
    )
)
async def echo_message_too(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    try:
        await message.forward(chat_id=message.chat.id)  # Пересылка сообщение
        # await message.copy_to(chat_id=message.chat.id) # Отправка копии
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new")


@router.message(
    F.text.lower().regexp(
        r"foo",
        mode=RegexpMode.SEARCH,
    )
)
async def echo_message_foo(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    text = "No FoO"
    await message.bot.send_message(  # Просто отправка сообщения без ответа или форварда
        chat_id=message.chat.id,
        text=text,
    )


@router.message(
    F.text.regexp(
        r"Bar",
        mode=RegexpMode.SEARCH,
    )
)
async def echo_message_bar(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    try:
        await message.forward(chat_id=message.chat.id)  # Пересылка сообщение
        # await message.copy_to(chat_id=message.chat.id) # Отправка копии
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new")





@router.message(
    F.photo,  # попадают только отправленные фото
    ~F.caption,  # Без подписи
)
async def handle_message_no_caption(message: types.Message):
    caption = "i can't see photo"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply_photo(
        photo=message.photo[-1].file_id,  # Основное фото всегда последнее
        caption=caption,  # Устанавливаем собственное описание
    )


@router.message(
    F.photo,  # Принимает фото
    F.caption.contains(
        "please"  # Где в описании фото есть слово "please" строгий регистр
    ),
)
async def handle_message_with_caption_please(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply(f"{str(message.caption)} please(0)")


@router.message(
    F.photo,
    F.caption,  # Есть подпись
    # ~F.caption, # ~ означает, что описания нет
)
async def handle_message_with_caption(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,  # id чата
        action=ChatAction.TYPING,  # Бот передает что набирает текст
    )
    await message.reply(f"{str(message.caption)} contains some text!")


@router.message(F.document | F.video)  # Принимает документы ИЛИ видео
async def handle_message_any_media(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    if message.document:
        await message.reply_document(
            document=message.document.file_id,
            caption=f"document {message.document.file_id}",
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id,
            caption=f"video {message.video.file_id}",
        )
    else:
        await message.reply("WTf is this?")


@router.message(
    F.from_user.id.in_({1756123777}),
    F.text.lower() == "secret",
)  # from_user.id.in_({1756123777}) - передается список пользователей,
# для которых доступна команда secret не чувствительна к регистру
async def secret_admin_message(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply("hellow, admin")


@router.message(
    F.text.regexp(
        r"\+7\(\d{3}\)(-\d{3})(-\d{2}){2}",
        mode=RegexpMode.SEARCH,
    ).as_("numder")
)
async def tel_message(message: types.Message, numder: Match[str]):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply(f"hellow, admin, {numder.group()}")