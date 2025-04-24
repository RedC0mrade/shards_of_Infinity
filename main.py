import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def handel_start(message: types.Message):
    await message.answer(text=f"Hello, {message.from_user.full_name}!")


@dp.message(Command("help"))
async def handel_help(message: types.Message):
    text = "I'm echo bot.\nSend me any"
    await message.answer(text=text)


@dp.message()
async def echo_message(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new")


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
