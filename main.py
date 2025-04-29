import asyncio
import logging
from re import Match

from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from magic_filter import RegexpMode

from config import settings

dp = Dispatcher()


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


# @dp.message(Command("code"))
# async def handle_command_code(message: types.Message):
#     text = markdown.text(
#         "Here`s Python code:",
#         "",
#         markdown.pre(
#             markdown.markdown_decoration.quote("print('Hello world!')"),
#             "python",
#         ),
#         sep="\n",
#     )
#     await message.answer(text=text)


@dp.message(F.photo, ~F.caption)
async def handle_message_no_caption(message: types.Message):
    await message.reply("i can't see photo")


@dp.message(F.photo, F.caption.contains("please"))
async def handle_message_with_caption(message: types.Message):
    await message.reply(f"{str(message.caption)} some text!")


@dp.message(F.document | F.video, F.caption)
async def handle_message_any_media(message: types.Message):
    await message.reply(
        f"{message.caption.lower()!r} {message.from_user.id} Some Video Or Photo"
    )


@dp.message(F.from_user.id.in_({1756123777}), F.text.lower() == "secret")
async def secret_admin_message(message: types.Message):
    await message.reply("hellow, admin")


@dp.message(
    F.text.regexp(
        r"\+7\(\d{3}\)(-\d{3})(-\d{2}){2}",
        mode=RegexpMode.SEARCH,
    ).as_("numder")
)
async def tel_message(message: types.Message, numder: Match[str]):
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
