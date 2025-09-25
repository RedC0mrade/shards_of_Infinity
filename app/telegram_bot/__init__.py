__all__ = ("router",)
from aiogram import Router

from app.telegram_bot.comands.start_comands import router as comands_router
from app.telegram_bot.comands.game_comands import router as game_router
from app.telegram_bot.comands.game_move_comands import router as move_router
from app.telegram_bot.comands.market_commands import router as market_router

router = Router()

router.include_routers(
    comands_router,
    game_router,
    move_router,
    market_router,
)
