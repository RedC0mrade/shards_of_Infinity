__all__ = ("router",)
from aiogram import Router

from .comands import router as comand_router
from .filters import router as filter_router
from .regexp import router as regexp_router

router = Router()

router.include_routers(
    filter_router,
    comand_router,
    regexp_router,
)
