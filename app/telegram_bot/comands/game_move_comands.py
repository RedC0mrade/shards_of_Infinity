from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.card import Card
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_crud import CardServices
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

    async with db_helper.session_context() as session:
        card_services = CardServices(session=session)
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
            return await callback.answer(text="Пожалуйста, дождитесь своего хода")

        card: Card = await card_services.get_hand_card(
            card_id=callback_data.id
        )  # Получаем карту, проверем в руке ли она

        if not card:
            logger.warning("Нет карты в руке id - %s", callback_data.id)
            return await callback.answer(
                text=(
                    "Скорее всего эта карта было уже разыграна, ",
                    "сделайте новый запрос карт в руке, ",
                    'с помощью кнопки "Рука"',
                )
            )

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
