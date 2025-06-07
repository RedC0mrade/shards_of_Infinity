import asyncio
import csv
import io
import logging
import aiohttp
from re import Match

from aiogram.utils.chat_action import ChatActionSender
from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction, ParseMode
from magic_filter import RegexpMode

from config import settings
from app.routers import router


dp = Dispatcher()
dp.include_router(router)

# @dp.message()
# async def echo_message(message: types.Message):
#     await message.copy_to(chat_id=message.chat.id)


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
