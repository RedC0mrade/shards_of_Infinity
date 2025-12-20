from pathlib import Path
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.card import Card, CardType
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.buy_move import BuyServices
from app.backend.crud.actions.champion_move import ChampionService
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.actions.game_move import MoveServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.telegram_bot.keyboards.champios_keyboard import ChampionCallback
from app.telegram_bot.keyboards.hand_keyboard import MarketCallback

from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.mersery_keyboard import play_mercenary
from app.utils.exceptions.exceptions import ChampionError
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


# id: int
# name: str
# champion_health: int


@router.callback_query(ChampionCallback.filter())
async def handle_attack_champion(
    callback: CallbackQuery,
    callback_data: ChampionCallback,
):
    async with db_helper.session_context() as session:

        card_instance_services = CardInstanceServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        champion_service = ChampionService(session=session)

        player_state: PlayerState = (
            await player_state_services.get_player_state_with_game(
                player_id=callback.from_user.id,
                active_player=True,
            )
        )

        card_instance: PlayerCardInstance = (
            card_instance_services.get_card_instance_for_id(
                card_instanse_id=callback_data.id
            )
        )

        if player_state.power < callback_data.champion_health:
            logger.info(
                "Ататка игорька - %s, здоровье чемпиона - %s",
                callback_data.champion_health,
                player_state.power,
            )

            raise ChampionError(
                message="Недостаточно очков атаки для уничтожения чемпиона"
            )
        player_state.power -= callback_data.champion_health
        card_instance.zone = CardZone.DISCARD

        session.commit()
