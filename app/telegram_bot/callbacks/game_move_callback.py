from __future__ import annotations

from pathlib import Path
from aiogram import Router, F, Bot
from typing import TYPE_CHECKING, Callable

from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InputMediaPhoto,
    InlineKeyboardMarkup,
)

from app.backend.core.models.card import Card, CardAction
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_crud import CardServices
from app.backend.crud.actions.game_move import MoveServices
from app.backend.crud.executors.effects_executor import EffectResult
from app.backend.crud.player_state_crud import PlayerStateServices

from app.telegram_bot.keyboards.dmcc_keyboard import CardCallback, KeyboardFactory

from app.backend.factories.database import db_helper
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


KEYBOARD_BY_ACTION: dict[
    CardAction,
    Callable[[list[PlayerCardInstance]], InlineKeyboardMarkup],
] = {
    CardAction.CHAMPION_DESTROY: KeyboardFactory.destroy_champion,
    CardAction.CARD_DESTROY: KeyboardFactory.destroy_card,
    CardAction.TAKE_CARD_FROM_MARKET: KeyboardFactory.market,
}


@router.callback_query(CardCallback.filter())
async def handle_play_card(
    callback: CallbackQuery,
    callback_data: CardCallback,
):
    """Обрабатываем команду розыгрыша карт"""

    logger.info("Обрабатываем команду розыгрыша карт")
    async with db_helper.session_context() as session:
        card_services = CardServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        move_services = MoveServices(session=session)

        player_state: PlayerState = (
            await player_state_services.get_player_state_with_game(
                player_id=callback.from_user.id,
                active_player=True,
            )
        )

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

        result: EffectResult = await move_services.make_move(
            card=card,
            player_state=player_state,
            game=player_state.game,
            player_id=callback.from_user.id,
        )

        if result:
            logger.debug("result - %s", result)
            logger.debug(
                "Обработка действия которое вернулось из effects_exector"
            )
            media = []
            for instace in result:
                card = instace.card
                logger.info(
                    "--------------------------Карта действия - %s", card.name
                )
                icon_path = media_dir / Path(instace.icon)
                media.append(
                    InputMediaPhoto(
                        media=FSInputFile(icon_path),
                    )
                )
            logger.info(
                "icon_path = %s exists=%s", icon_path, icon_path.exists()
            )

            if len(media) == 1:
                logger.info("Карта только 1")
                await callback.bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=media[0].media,
                )
            else:
                logger.info("чемпионов больше 1")
                await callback.bot.send_media_group(
                    chat_id=callback.message.chat.id,
                    media=media,
                )
            logger.info("отработал колбэк с медиа- %s", media)
            await callback.message.answer(
                text="",
                reply_markup=KeyboardFactory(result.instance),
            )
            logger.info("Отработала клавиатура")
            return

        photo = FSInputFile(media_dir / Path(card.icon))

        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы сыграли карту {card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник разыграл карту: {card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
