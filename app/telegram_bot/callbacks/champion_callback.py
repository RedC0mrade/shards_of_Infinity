from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.champion_move import ChampionServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.telegram_bot.dependencies.dependencies import Services
from app.telegram_bot.keyboards.dmcc_keyboard import (
    AttackChampionCallback,
    DestroyChampionCallback,
)

from app.backend.factories.database import db_helper
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(AttackChampionCallback.filter())
async def handle_attack_champion(
    callback: CallbackQuery,
    callback_data: AttackChampionCallback,
    services: Services,
):
    await callback.message.edit_reply_markup(reply_markup=None)

    player_state: PlayerState = (
        await services.player_state.get_player_state_with_game(
            player_id=callback.from_user.id,
            active_player=True,
        )
    )
    logger.info("Получили player_state - %s", player_state)
    card_instance: PlayerCardInstance = (
        await services.card_instance.get_card_instance_for_id(
            card_instanse_id=callback_data.id
        )
    )
    logger.info("Получили card_instance - %s", card_instance)
    await services.champion.attack_the_champion(
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
    await services.session.commit()


@router.callback_query(DestroyChampionCallback.filter())
async def handle_destroy_champion(
    callback: CallbackQuery,
    callback_data: DestroyChampionCallback, services: Services,
):

    await callback.message.edit_reply_markup(reply_markup=None)

    player_state: PlayerState = (
        await services.player_state.get_player_state_with_game(
            player_id=callback.from_user.id,
            active_player=True,
        )
    )
    logger.info("Получили player_state - %s", player_state)
    card_instance: PlayerCardInstance = (
        await services.card_instance.get_card_instance_for_id(callback_data.id)
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
    await services.session.commit()
