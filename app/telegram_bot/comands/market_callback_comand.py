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
from app.telegram_bot.keyboards.hand_keyboard import MarketCallback

from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.mersery_keyboard import play_mercenary
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)


@router.callback_query(MarketCallback.filter())
async def handle_buy_card(
    callback: CallbackQuery,
    callback_data: MarketCallback,
):

    async with db_helper.session_context() as session:
        card_instanse_service = CardInstanceServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        buy_service = BuyServices(session=session)

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

        card_instance: PlayerCardInstance = (
            await card_instanse_service.get_card_instance_in_some_card_zone(
                game_id=player_state.game_id,
                card_id=callback_data.id,
                card_zone=CardZone.MARKET,
            )
        )  # Получаем id карты, проверем находится ли она на рынке

        if not card_instance:
            logger.warning("Нет карты на рынке с id - %s", callback_data.id)
            return await callback.answer(
                text=(
                    "Эта карта было уже куплена, "
                    "сделайте новый запрос карт рынка, "
                    'с помощью кнопки "Рынок"'
                )
            )


        photo = FSInputFile(card_instance.card.icon)

        # Обрабатываем случай, если карта наёмник
        if card_instance.card.card_type == CardType.MERCENARY:
            await callback.message.answer_photo(
                photo=photo,
                caption="Вы купили карту наемника, выберите как её сыграть",
                reply_markup=play_mercenary(
                    card_instance_id=card_instance.id,
                    player_state_id=player_state.id,
                    game_id=player_state.game_id,
                    card_id=card_instance.card.id,
                ),
            )
            return

        answer = await buy_service.buy_card_from_market(
            card_instance=card_instance,
            card=card_instance.card,
            player_state=player_state,
            game=player_state.game,
            player_id=callback.from_user.id,
        )
        if answer[0]:
            await callback.message.answer_photo(
                photo=photo,
                caption=f"Вы купили карту {card_instance.card.name}",
            )
            await callback.bot.send_photo(
                photo=photo,
                caption=f"Ваш противник купил карту: {card_instance.card.name}",
                chat_id=player_state.game.non_active_player_id,
            )
        else:
            await callback.message.answer(text=answer[1])
