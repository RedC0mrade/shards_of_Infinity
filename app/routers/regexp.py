from re import Match

from aiogram.utils.chat_action import ChatActionSender
from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction, ParseMode
from magic_filter import RegexpMode

router = Router(name=__name__)

@router.message(F.text.regexp(
        r"Card\s#[1-6]",
        mode=RegexpMode.SEARCH,
        ).as_("card_id")
)
async def send_card(message: types.Message, card_id: Match[str]):
    async with ChatActionSender(  # ChatActionSender чат экшен работает все время пока отправляется фаил
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    ):
        cart_number = card_id.group()[-1]
        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=types.FSInputFile(
                path=f"C:/telegram/shards_{cart_number}.jpg"
            ),
            caption=f"Описание карты номер {cart_number}"
        )


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