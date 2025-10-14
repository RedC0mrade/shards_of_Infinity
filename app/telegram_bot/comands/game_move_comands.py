from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.card import Card
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.game_move_crud import MoveServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.telegram_bot.keyboards.hand_keyboard import CardCallback

from app.backend.factories.database import db_helper
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)


@router.callback_query(CardCallback.filter())
async def handle_play_card(
    callback: CallbackQuery,
    callback_data: CardCallback,
):
    """Обрабатываем команду розыгрыша карт"""

    logger.info("Обрабатываем команду розыгрыша карт")
    async with db_helper.session_context() as session:
        card_services = CardServices(session=session)
        # card_instance_services = CardInstanceServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        move_services = MoveServices(session=session)

        player_state: PlayerState = (
            await player_state_services.get_player_state_with_game(
                player_id=callback.from_user.id
            )
        )
        if player_state.game.active_player_id != callback.from_user.id:
            logger.warning(
                "active_player_id = %s, callback.from_user.id = %s",
                player_state.game.active_player_id,
                callback.from_user.id,
            )
            await callback.answer(text="Пожалуйста, дождитесь своего хода")
            return

        card: Card = await card_services.get_hand_card(
            player_state_id=player_state.id,
            card_id=callback_data.id,
            card_zone=CardZone.HAND,
            game_id=player_state.game_id,
        )  # Получаем карту, только если она в руке
        if not card:

            logger.warning("Нет карты в руке id - %s", callback_data.id)
            return await callback.answer(
                text=(
                    "Эта карта была уже разыграна, "
                    "сделайте новый запрос карт в руке, "
                    'с помощью кнопки "Рука"'
                )
            )
        logger.info("Получили карту %s c id - %s", card.name, card.id)

        await move_services.make_move(
            card=card,
            player_state=player_state,
            game=player_state.game,
            player_id=callback.from_user.id,
        )

        photo = FSInputFile(card.icon)

        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы сыграли карту {card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник разыграл карту: {card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
