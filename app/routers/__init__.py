__all__ = ("router",)
from aiogram import Router

from .comands import router as comand_router
from .filters import router as filter_router

router = Router()

router.include_router(comand_router)
router.include_router(filter_router)
