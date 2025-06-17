from re import Match

from aiogram.utils.chat_action import ChatActionSender
from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction, ParseMode
from aiogram.types import ReplyKeyboardRemove
from magic_filter import RegexpMode
from config import settings
from app.keyboards.common_keyboards import ButtonText

router = Router(name=__name__)


@router.message(F.text == ButtonText.BYE)
async def handle_bye(message: types.Message):
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=f"Bye {message.from_user.first_name}",
        reply_markup=ReplyKeyboardRemove(),  # Удаление клавиатуры у клиента
    )


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
    F.from_user.id.in_(settings.admin_ids),
    F.text.lower() == "secret",
)  # from_user.id.in_({1756123777}) - передается список пользователей,
# для которых доступна команда secret не чувствительна к регистру
async def secret_admin_message(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply("hellow, admin")

