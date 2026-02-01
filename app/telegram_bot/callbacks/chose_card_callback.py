from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.buy_move import BuyServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.factories.database import db_helper
from app.telegram_bot.keyboards.dmcc_keyboard import ChooseCardCallback
from app.utils.exceptions.exceptions import GameError
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(ChooseCardCallback.filter())
async def handle_choose_card(
    callback: CallbackQuery,
    callback_data: ChooseCardCallback,
):
    """Обработка карты портальный монах"""
    async with db_helper.session_context() as session:

        card_instance_services = CardInstanceServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        buy_service = BuyServices(session=session)

        player_state: PlayerState = (
            await player_state_services.get_player_state_with_game(
                player_id=callback.from_user.id,
                active_player=True,
            )
        )
        card_instance: PlayerCardInstance = (
            await card_instance_services.get_card_instance_for_id(
                card_instanse_id=callback_data.id
            )
        )
        photo = FSInputFile(media_dir / Path(card_instance.card.icon))

        if not card_instance.position_on_market:
            raise GameError(
                "Эта карта уже была разыграна. "
                "Сделайте новый запрос рынка через кнопку «Рынок». 🛒"
            )
        position_on_market = card_instance.position_on_market
        card_instance.position_on_market = None
        card_instance.player_state_id = callback.from_user.id
        
        await buy_service.replacement_cards_from_the_market(
            game_id=player_state.game_id,
            position_on_market=position_on_market,
        )
        
        if player_state.mastery >= 15:
            card_instance.zone = CardZone.HAND
            await callback.message.answer_photo(
                photo=photo,
                caption=f"Вы получили в руку карту: {card_instance.card.name}",
            )
            await callback.bot.send_photo(
                photo=photo,
                caption=f"Ваш противник получили в руку карту: {card_instance.card.name}",
                chat_id=player_state.game.non_active_player_id,
            )
        else:
            card_instance.zone = CardZone.DISCARD
            await callback.message.answer_photo(
                photo=photo,
                caption=f"Вы выбрали карту: {card_instance.card.name}",
            )
            await callback.bot.send_photo(
                photo=photo,
                caption=f"Ваш противник выбрал карту: {card_instance.card.name}",
                chat_id=player_state.game.non_active_player_id,
            )
        await session.commit()
