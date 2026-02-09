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
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.telegram_bot.keyboards.dmcc_keyboard import KeyboardFactory
from app.telegram_bot.keyboards.dmcc_keyboard import MarketCallback

from app.backend.factories.database import db_helper
from app.utils.exceptions.exceptions import MarketError, NotYourTurn
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(MarketCallback.filter())
async def handle_buy_card(
    callback: CallbackQuery,
    callback_data: MarketCallback,
):

    async with db_helper.session_context() as session:
        card_instance_service = CardInstanceServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        buy_service = BuyServices(session=session)
        card_instance: PlayerCardInstance = (
            await card_instance_service.get_card_instance_for_id(
                card_instanse_id=callback_data.id
            )
        )
        player_state: PlayerState = (
            await player_state_services.get_player_state_with_game(
                player_id=callback.from_user.id
            )
        )
        logger.info(
            "Зона - %s, Название карты - %s",
            card_instance.zone,
            card_instance.card.name,
        )
        if player_state.game.active_player_id != callback.from_user.id:
            logger.warning(
                "active_player_id = %s, callback.from_user.id = %s",
                player_state.game.active_player_id,
                callback.from_user.id,
            )
            raise NotYourTurn(message="Пожалуйста, дождитесь своего хода")

        if card_instance.zone != CardZone.MARKET:
            logger.warning("Нет карты на рынке с id - %s", callback_data.id)
            raise MarketError(
                message=(
                    "Эта карта было уже куплена, "
                    "сделайте новый запрос карт рынка, "
                    'с помощью кнопки "Рынок"'
                )
            )

        photo = FSInputFile(media_dir / Path(card_instance.card.icon))

        # Обрабатываем случай, если карта наёмник
        logger.info("Тип карты - %s", card_instance.card.card_type)
        if card_instance.card.card_type == CardType.MERCENARY:
            logger.info("Карта является наемником")
            await callback.message.answer_photo(
                photo=photo,
                caption="Вы купили карту наемника, выберите как её сыграть",
                reply_markup=KeyboardFactory.mercenary(
                    card_instance_id=card_instance.id
                ),
            )
            return

        await buy_service.buy_card_from_market(
            card_instance=card_instance,
            card=card_instance.card,
            player_state=player_state,
            game=player_state.game,
            player_id=callback.from_user.id,
        )
        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы купили карту {card_instance.card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник купил карту: {card_instance.card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
