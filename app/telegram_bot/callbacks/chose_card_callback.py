from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery

from app.telegram_bot.keyboards.dmcc_keyboard import ChooseCardCallback
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"

@router.callback_query(ChooseCardCallback.filter())
async def handle_choose_card(
    callback: CallbackQuery,
    callback_data: ChooseCardCallback,
):
    """Обработка карты портальный монах"""