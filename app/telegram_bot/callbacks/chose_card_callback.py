from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery

from app.backend.core.models.play_card_instance import CardZone, PlayerCardInstance
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.factories.database import db_helper
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
    async with db_helper.session_context() as session:

        card_instance_services = CardInstanceServices(session=session)
        player_state_services = PlayerStateServices(session=session)

        player_state: PlayerState = await (
            player_state_services.get_player_state_with_game(
                player_id=callback.from_user.id,
                active_player=True,
            )
        )
        card_instance: PlayerCardInstance = await (
            card_instance_services.get_card_instance_for_id(
                card_instanse_id=callback_data.id
            )
        )

        if player_state.mastery >= 15:
            card_instance.zone = CardZone.HAND
        else:
            card_instance.zone = CardZone.DISCARD
        await session.commit()
        
