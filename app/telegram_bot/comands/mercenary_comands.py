from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.card import Card, CardType
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.buy_move import BuyServices
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.game_move_crud import MoveServices
from app.backend.crud.player_state_crud import PlayerStateServices

from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.mersery_keyboard import MercenaryCallback
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)

#     card_instance_id: int
#     play_now: bool
#     player_state_id: int
#     game_id: int
#     card_id: int


@router.callback_query(MercenaryCallback.filter())
async def mercenary_play(
    callback: CallbackQuery,
    callback_data: MercenaryCallback,
):
    async with db_helper.session_context() as session:

        card_instance_services = CardInstanceServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        move_services = MoveServices(session=session)
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
            return await callback.answer(
                text="Пожалуйста, дождитесь своего хода"
            )

        card_instance: PlayerCardInstance = (
            await card_instance_services.get_card_inctance_for_id(
                card_instanse_id=callback_data.card_instance_id,
            )
        )
        if not card_instance:
            logger.warning(
                "Нет карты наёмника на рынке - id - %s",
                callback_data.card_instance_id,
            )
            return await callback.answer(
                text=(
                    "Эта карта было уже разыграна, ",
                    "сделайте новый запрос рынка, ",
                    'с помощью кнопки "Рынок"',
                )
            )
        if card_instance.zone != CardZone.MARKET:
            logger.warning("Неверная зона карты - %s", card_instance.zone)

        photo = FSInputFile(card_instance.card.icon)

        if callback_data.play_now:
            position_on_market = card_instance.position_on_market
            answer = await move_services.make_move(
                card=card_instance.card,
                player_state=player_state,
                game=player_state.game,
                player_id=callback.from_user.id,
                mercenary=True,
            )
            logger.info("Отработка карты покупки наемника ответ %s", answer)
            await buy_service.replacement_cards_from_the_market(
                game_id=player_state.game_id,
                position_on_market=position_on_market,
            )
            if not answer:
                return await callback.message.answer(text=answer)

            await callback.message.answer_photo(
                photo=photo,
                caption=f"Вы сыграли карту {card_instance.card.name}",
            )
            await callback.bot.send_photo(
                photo=photo,
                caption=f"Ваш противник разыграл карту: {card_instance.card.name}",
                chat_id=player_state.game.non_active_player_id,
            )
        else:
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
