from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from config import settings
from app.backend.api.card import router as card_router

router = APIRouter(prefix=settings.api_prefix.prefix)
router.include_router(card_router)