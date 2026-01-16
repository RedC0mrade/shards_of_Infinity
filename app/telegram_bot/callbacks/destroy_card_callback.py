from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.play_card_instance import PlayerCardInstance
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.champion_move import ChampionService
from app.backend.crud.actions.destroy_card_move import DestroyCardService
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.dmcc_keyboard import DestroyCardCallback
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(DestroyCardCallback.filter())
async def handle_card_destroy(
    callback: CallbackQuery, callback_data: DestroyCardCallback
):
    async with db_helper.session_context as session:

        card_instance_service = CardInstanceServices(session=session)
        player_state_service = PlayerStateServices(session=session)
        destroy_card_service = DestroyCardService(session=session)
        player_state: PlayerState = (
            await player_state_service.get_player_state_with_game(
                player_id=callback.from_user.id,
                active_player=True,
            )
        )
        logger.info("Получили player_state - %s", player_state)
        card_instance: PlayerCardInstance = (
            await card_instance_service.get_card_instance_for_id(
                card_instanse_id=callback_data.id
            )
        )
        logger.info("Получили card_instance - %s", card_instance)
