import asyncio
import logging
import uvicorn

from fastapi import FastAPI

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from fastapi.concurrency import asynccontextmanager

from config import settings
from app.telegram_bot import router as bot_router
from app.backend.api import router as api_router
from app.backend.factories.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация бота при старте
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(bot_router)
    
    # Запускаем поллинг в фоне
    asyncio.create_task(dp.start_polling(bot))
    
    yield
    
    # Очистка при завершении
    await bot.session.close()
    await db_helper.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(
    api_router,
    prefix=settings.api_prefix.prefix,
)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )