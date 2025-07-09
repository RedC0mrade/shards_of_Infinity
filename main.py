import asyncio
import logging
import uvicorn

from fastapi import FastAPI

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from fastapi.concurrency import asynccontextmanager

from config import settings
from app.routers import router
from app.backend.factories.database import db_helper


@asynccontextmanager
async def lifepan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifepan)


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
