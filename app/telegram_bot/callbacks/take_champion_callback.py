from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.telegram_bot.dependencies.dependencies import Services
from app.telegram_bot.keyboards.dmcc_keyboard import (
    TakeChampionyCallback,
)
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(TakeChampionyCallback.filter())
async def handle_choose_card(
    callback: CallbackQuery,
    callback_data: TakeChampionyCallback,
    services: Services,
):
    """Обработка карты Легинер Корвус"""
    
    logger.info("Обрабатываем коллбэк Легинер Корвус")

    await callback.message.edit_reply_markup(reply_markup=None)

    champion: PlayerCardInstance = (
        await services.card_instance.get_card_instance_for_id(
            card_instanse_id=callback_data.id
        )
    )

    champion.zone = CardZone.HAND

    await services.session.commit()
