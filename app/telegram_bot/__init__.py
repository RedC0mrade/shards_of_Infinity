__all__ = ("router",)
from aiogram import Router

from app.telegram_bot.comands.start_comands import router as comands_router
from app.telegram_bot.comands.game_comands import router as game_router
from app.telegram_bot.comands.game_move_comands import router as move_router
from app.telegram_bot.comands.market_callback_comand import router as market_router
from app.telegram_bot.comands.mercenary_comands import router as mercenary_router
from app.telegram_bot.comands.champion_callback import router as champion_router
router = Router()

router.include_routers(
    comands_router,
    game_router,
    move_router,
    market_router,
    mercenary_router,
    champion_router,
)
