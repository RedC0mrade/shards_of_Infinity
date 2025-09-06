from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.card import Card
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_crud import CardServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.telegram_bot.keyboards.hand_keyboard import CallBackCard

from app.backend.factories.database import db_helper
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)


@router.callback_query(CallBackCard.filter())
async def handle_play_card(
    callback: CallbackQuery,
    callback_data: CallBackCard,
):

    async with db_helper.session_context() as session:
        card_services = CardServices(session=session)
        player_state_services = PlayerStateServices(session=session)

        player_state: PlayerState = await player_state_services.get_game(
            player_id=callback.from_user.id
        )
        if player_state.game.active_player_id != callback.from_user.id:
            logger.warning(
                "active_player_id = %s, callback.from_user.id = %s",
                player_state.game.active_player_id,
                callback.from_user.id,
            )
            await callback.answer(text="Пожалуйста, дождитесь своего хода")
            return

        card: Card = await card_services.get_card(card_id=callback_data.id)

        photo = FSInputFile(card.icon)

        await callback.message.answer_photo(
            photo=photo, caption=f"Вы сыграли карту {card.name}"
        )
        await callback.bot.send_photo(
            photo=photo, caption=f"Ваш противник разыграл карту: {card.name}"
        )
