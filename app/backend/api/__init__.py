from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from config import settings
from app.backend.api.card_api import router as card_router
from app.backend.api.user_api import router as user_router


router = APIRouter(prefix=settings.api_prefix.prefix)
router.include_router(card_router)
router.include_router(user_router)