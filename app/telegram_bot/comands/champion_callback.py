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
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.actions.game_move import MoveServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.telegram_bot.keyboards.champios_keyboard import ChampionCallback
from app.telegram_bot.keyboards.hand_keyboard import MarketCallback

from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.mersery_keyboard import play_mercenary
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(ChampionCallback.filter())
async def handle_attack_champion(
    callback: CallbackQuery,
    callback_data: ChampionCallback,
):