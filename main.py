import asyncio
import io
import logging
from re import Match

from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ChatAction, ParseMode
from magic_filter import RegexpMode

from config import settings

dp = Dispatcher()


@dp.message(Command("test"))
async def send_text_file(message: types.Message):
    file = io.StringIO()
    message.bot.send_document(
        chat_id=message.chat.id,
        document=types.BufferedInputFile(
            file=...,
            filename="text.txt",
        ),
    )


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    url = "https://cf.geekdo-images.com/GfQBoqOl21zQx-Vy-dSHZw__imagepagezoom/img/5cxdPGDSaEhGGm1lLkFGKt3-2iE=/fit-in/1200x900/filters:no_upscale():strip_icc()/pic4064509.png"
    await message.answer(
        text=f"{markdown.hide_link(url)}Hello, {markdown.hbold(message.from_user.full_name)}!",
        parse_mode=ParseMode.HTML,
    )


@dp.message(Command("help"))
async def handel_help(message: types.Message):

    text = markdown.text(
        markdown.markdown_decoration.quote("I'm an echo bot."),
        markdown.text(
            markdown.markdown_decoration.italic(markdown.bold("Send")),
            markdown.markdown_decoration.quote(" me any!"),
            ParseMode=ParseMode.MARKDOWN_V2,
        ),
        sep="\n",
    )
    await message.answer(text=text)


# @dp.message(F.photo, ~F.caption)
# async def handle_message_no_caption(message: types.Message):
#     await message.reply("i can't see photo")


@dp.message(Command("pic"))
async def handel_command_pic(message: types.Message):
    url = "https://img.freepik.com/free-vector/sweet-eyed-kitten-cartoon-character_1308-135596.jpg?semt=ais_hybrid&w=740"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    await message.reply_photo(
        photo=url,
        caption="cat photo",
    )


@dp.message(Command("home_pic"))
async def handel_command_home_pic(message: types.Message):
    file_path = "C:/Users/e2e4e/Pictures/IMG_20240802_183555[1].jpg"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    await message.reply_photo(
        photo=types.FSInputFile(
            path=file_path,
        ),
        caption="cat photo",
    )


@dp.message(Command("file"))
async def handel_command_file(message: types.Message):
    file_path = "C:/Users/e2e4e/Downloads/zapret-discord-youtube-1.7.2b.rar"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    message_send = await message.reply_document(
        document=types.FSInputFile(path=file_path, filename="antizapret"),
        caption="Antizapret",
    )
    print(
        message_send.document.file_id
    )  # id для сохранения в базе и отправки повторно


@dp.message(F.photo, ~F.caption)
async def handle_message_no_caption(message: types.Message):
    caption = "i can't see photo"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=caption,
    )


@dp.message(F.photo, F.caption.contains("please"))
async def handle_message_with_caption_please(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply(f"{str(message.caption)} please(0)")


@dp.message(F.photo, F.caption)
async def handle_message_with_caption(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply(f"{str(message.caption)} contains some text!")


@dp.message(F.document | F.video)
async def handle_message_any_media(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    if message.document:
        await message.reply_document(
            document=message.document.file_id,
            caption="document",
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id,
            caption="video",
        )
    else:
        await message.reply("WTf is this?")


@dp.message(F.from_user.id.in_({1756123777}), F.text.lower() == "secret")
async def secret_admin_message(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply("hellow, admin")


@dp.message(
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


@dp.message()
async def echo_message(message: types.Message):
    try:
        await message.forward(chat_id=message.chat.id)
        # await message.copy_to(chat_id=message.chat.id)
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
