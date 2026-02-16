from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.buy_move import BuyServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.dmcc_keyboard import (
    ChooseCardCallback,
    TakeChampionyCallback,
)
from app.utils.exceptions.exceptions import GameError
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(TakeChampionyCallback.filter())
async def handle_choose_card(
    callback: CallbackQuery,
    callback_data: TakeChampionyCallback,
):
    """Обработка карты Легинер Корвус"""
    logger.info("Обрабатываем коллбэк Легинер Корвус")

    await callback.message.edit_reply_markup(reply_markup=None)
    async with db_helper.session_context() as session:

        card_instance_service = CardInstanceServices(session=session)
        champion: PlayerCardInstance = await card_instance_service.get_card_instance_for_id(
            card_instanse_id=callback_data.id
        )

        champion.zone = CardZone.HAND

        await session.commit()
