import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode

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


@dp.message()
async def echo_message(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
