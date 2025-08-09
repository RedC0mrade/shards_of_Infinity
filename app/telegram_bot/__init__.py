__all__ = ("router",)
from aiogram import Router

from app.telegram_bot.comands.comands import router as comands_router

router = Router()

router.include_routers(
    comands_router,
)
