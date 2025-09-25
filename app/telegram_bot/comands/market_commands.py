from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.game_move_keyboard import MoveKBText
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
