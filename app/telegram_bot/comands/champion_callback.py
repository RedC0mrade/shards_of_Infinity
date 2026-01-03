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
from app.backend.crud.executors.ps_count_executor import PlayStateExecutor
from app.backend.crud.player_state_crud import PlayerStateServices
from app.telegram_bot.keyboards.champios_keyboard import (
    AtackChampionCallback,
    DestroyChampionCallback,
)
from app.telegram_bot.keyboards.hand_keyboard import MarketCallback

from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.mersery_keyboard import play_mercenary
from app.utils.exceptions.exceptions import ChampionError
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


# id: int
# champion_health: int


@router.callback_query(AtackChampionCallback.filter())
async def handle_attack_champion(
    callback: CallbackQuery,
    callback_data: AtackChampionCallback,
):
    async with db_helper.session_context() as session:

        card_instance_service = CardInstanceServices(session=session)
        player_state_service = PlayerStateServices(session=session)
        champion_service = ChampionService(session=session)

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
        await champion_service.attack_the_champion(
            card_instance=card_instance,
            player_state=player_state,
        )
        logger.info("Функция attack_the_champion отработала")
        photo = FSInputFile(media_dir / Path(card_instance.card.icon))

        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы уничтожили чемпиона {card_instance.card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник уничтожили чемпиона: {card_instance.card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
        await session.commit()


@router.callback_query(DestroyChampionCallback.filter())
async def handle_destroy_champion(
    callback: CallbackQuery,
    callback_data: DestroyChampionCallback,
):
    async with db_helper.session_context() as session:

        card_instance_service = CardInstanceServices(session=session)
        player_state_service = PlayerStateServices(session=session)
        player_state: PlayerState = (
            await player_state_service.get_player_state_with_game(
                player_id=callback.from_user.id,
                active_player=True,
            )
        )
        logger.info("Получили player_state - %s", player_state)
        card_instance: PlayerCardInstance = (
            await card_instance_service.get_card_instance_for_id(
                callback_data.id
            )
        )

        card_instance.zone = CardZone.DISCARD
        photo = FSInputFile(media_dir / Path(card_instance.card.icon))
        logger.info("Функция attack_the_champion отработала")
        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы уничтожили чемпиона {card_instance.card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник уничтожили чемпиона: {card_instance.card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
        await session.commit()
