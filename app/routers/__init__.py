__all__ = ("router",)
from aiogram import Router

from .comands import router as comand_router
from .filters import router as filter_router
from .regexp import router as regexp_router
from .commands_for_inline_keyboard import router as inline_router
from .callback_data import router as callback_data_router

router = Router()

router.include_routers(
    callback_data_router,
    inline_router,
    filter_router,
    comand_router,
    regexp_router,
)
