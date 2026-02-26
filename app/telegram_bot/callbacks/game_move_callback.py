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
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.executors.effects_executor import EffectResult
from app.backend.crud.player_state_crud import PlayerStateServices

from app.telegram_bot.keyboards.dmcc_keyboard import (
    CardCallback,
    KeyboardFactory,
)

from app.backend.factories.database import db_helper
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


KEYBOARD_BY_ACTION: dict[
    CardAction,
    Callable[[list[PlayerCardInstance]], InlineKeyboardMarkup],
] = {
    CardAction.CHOOSE_CARD_FROM_MARKET: KeyboardFactory.choose_card,
    CardAction.CHAMPION_DESTROY: KeyboardFactory.destroy_champion,
    CardAction.CARD_DESTROY: KeyboardFactory.destroy_card,
    CardAction.TAKE_CARD_FROM_MARKET: KeyboardFactory.market,
    CardAction.TAKE_CHAMPION_FROM_RESET: KeyboardFactory.take_champion,
}


@router.callback_query(CardCallback.filter())
async def handle_play_card(
    callback: CallbackQuery,
    callback_data: CardCallback,
):
    """Обрабатываем команду розыгрыша карт"""

    await callback.message.edit_reply_markup(reply_markup=None)

    logger.info("Обрабатываем команду розыгрыша карт")
    async with db_helper.session_context() as session:
        card_services = CardServices(session=session)
        player_state_services = PlayerStateServices(session=session)
        move_services = MoveServices(session=session)
        card_instance_service = CardInstanceServices(session=session)
        player_state: PlayerState = (
            await player_state_services.get_player_state_with_game(
                player_id=callback.from_user.id,
                active_player=True,
            )
        )
        card_instance_service
        logger.info(
            "\n------player_state_id - %s\n------card_id - %s\n------card_zone - %s\n------game_id - %s",
            player_state.id,
            callback_data.id,
            CardZone.HAND,
            player_state.game_id,
        )
        card_instance: PlayerCardInstance = (
            await card_instance_service.get_card_instance_for_id(
                card_instanse_id=callback_data.id
            )
        )

        if (
            card_instance.zone != CardZone.HAND
            or card_instance.game_id != player_state.game_id
        ):

            logger.warning("Нет карты в руке id - %s", callback_data.id)
            return await callback.answer(
                text=(
                    "Эта карта была уже разыграна, "
                    "сделайте новый запрос карт в руке, "
                    'с помощью кнопки "Рука"'
                )
            )
        logger.info(
            "Получили карту %s c id - %s",
            card_instance.card.name,
            card_instance.card.id,
        )

        result: EffectResult = await move_services.make_move(
            card=card_instance.card,
            player_state=player_state,
            game=player_state.game,  # нужно ли? Есть в PlayerState
            player_id=callback.from_user.id,
        )

        if result:
            logger.debug("result - %s", result)
            logger.debug("Обработка действия которое вернулось из effects_exector")
            media = []
            for instace in result.instance:
                logger.info(
                    "--------------------------Карта действия - %s",
                    instace.card.name,
                )
                icon_path = media_dir / Path(instace.card.icon)
                media.append(
                    InputMediaPhoto(
                        media=FSInputFile(icon_path),
                    )
                )
            logger.info("icon_path = %s exists=%s", icon_path, icon_path.exists())
            keyboard_factory = KEYBOARD_BY_ACTION.get(result.action)
            if len(media) == 1:
                logger.info("Карта только 1")
                await callback.bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=media[0].media,
                )
            else:
                logger.info("Карт больше 1")
                await callback.bot.send_media_group(
                    chat_id=callback.message.chat.id,
                    media=media,
                )
            logger.info("отработал колбэк с медиа- %s", media)
            await callback.message.answer(
                text="Выберите карту",
                reply_markup=keyboard_factory(result.instance),
            )
            logger.info("Отработала клавиатура")
            return

        photo = FSInputFile(media_dir / Path(card_instance.card.icon))

        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы сыграли карту {card_instance.card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник разыграл карту: {card_instance.card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
