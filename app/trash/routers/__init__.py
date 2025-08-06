__all__ = ("router",)
from aiogram import Router

from .comands import router as comand_router
from .filters import router as filter_router
from .regexp import router as regexp_router
from .commands_for_inline_keyboard import router as inline_router
from .callback_data_router import router as callback_router
from .shop_commands import router as shop_router
from .shop_kb_callback_handlers import router as shop_kb_router
from .survey import router as survey_router
router = Router()

router.include_routers(
    survey_router,
    callback_router,
    inline_router,
    filter_router,
    comand_router,
    regexp_router,
    shop_router,
    shop_kb_router,
)
