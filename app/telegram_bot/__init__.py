__all__ = ("router",)
from aiogram import Router

from app.telegram_bot.comands.start_comands import router as comands_router
from app.telegram_bot.comands.game_comands import router as game_router
from app.telegram_bot.callbacks.game_move_callback import router as move_router
from app.telegram_bot.callbacks.market_callback import router as market_router
from app.telegram_bot.callbacks.mercenary_callback import router as mercenary_router
from app.telegram_bot.callbacks.champion_callback import router as champion_router
from app.telegram_bot.callbacks.chose_card_callback import router as choose_router
from app.telegram_bot.callbacks.destroy_card_callback import router as destroy_router
router = Router()

router.include_routers(
    comands_router,
    game_router,
    move_router,
    market_router,
    mercenary_router,
    champion_router,
    destroy_router,
    choose_router,
    
)
