from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState

from app.telegram_bot.dependencies.dependencies import Services
from app.telegram_bot.keyboards.dmcc_keyboard import (
    MercenaryCallback,
    TakeMercenaryCallback,
)
from app.utils.exceptions.exceptions import GameError
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(MercenaryCallback.filter())
async def mercenary_play(
    callback: CallbackQuery,
    callback_data: MercenaryCallback,
    services: Services,
):
    await callback.message.edit_reply_markup(reply_markup=None)

    logger.info("Стартуем обработку mercenary_play")
    player_state: PlayerState = (
        await services.player_state.get_player_state_with_game(
            player_id=callback.from_user.id,
            active_player=True,
        )
    )
    logger.info("Начинаем обработку меню наемника")
    card_instance: PlayerCardInstance = (
        await services.card_instance.get_card_instance_for_id(
            card_instanse_id=callback_data.id,
        )
    )
    logger.info("Получити card_instance с id - %s", card_instance.id)
    if not card_instance:
        logger.warning(
            "Нет карты наёмника на рынке - id - %s",
            callback_data.id,
        )
        raise GameError(
            "Эта карта уже была разыграна. "
            "Сделайте новый запрос рынка через кнопку «Рынок». 🛒"
        )
    if card_instance.zone != CardZone.MARKET:
        logger.warning("Неверная зона карты - %s", card_instance.zone)
        raise GameError("Эта карта уже не находится на рынке. 🃏")

    photo = FSInputFile(media_dir / Path(card_instance.card.icon))

    if callback_data.play_now:
        logger.info("callback_data.play_now = True")
        position_on_market = card_instance.position_on_market
        card_instance.player_state_id = player_state.id

        await services.move.make_move(
            card=card_instance.card,
            player_state=player_state,
            game=player_state.game,
            player_id=callback.from_user.id,
            mercenary=True,
        )
        logger.info("Надеюсь у наемников не будет сложных спэлов")
        await services.buy.replacement_cards_from_the_market(
            game_id=player_state.game_id,
            position_on_market=position_on_market,
        )
        logger.info("Заменили карту на рынке")

        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы сыграли карту {card_instance.card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник разыграл карту: {card_instance.card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
        card_instance.delete_mercenary = True
        logger.info("Изменяем delete_mercenary на True")

    else:
        logger.info("callback_data.play_now = False")
        await services.buy.buy_card_from_market(
            card_instance=card_instance,
            card=card_instance.card,
            player_state=player_state,
            game=player_state.game,
            player_id=callback.from_user.id,
        )
        logger.info("Отработала buy_card_from_market")
        await callback.message.answer_photo(
            photo=photo,
            caption=f"Вы купили карту {card_instance.card.name}",
        )
        await callback.bot.send_photo(
            photo=photo,
            caption=f"Ваш противник купил карту: {card_instance.card.name}",
            chat_id=player_state.game.non_active_player_id,
        )
    logger.info("Выполняем коммит")
    await services.session.commit()


@router.callback_query(TakeMercenaryCallback.filter())
async def take_mercenary(
    callback: CallbackQuery,
    callback_data: TakeMercenaryCallback,
    services: Services,
):

    logger.info("Стартуем обработку take_mercenary")
    player_state: PlayerState = (
        await services.player_state.get_player_state_with_game(
            player_id=callback.from_user.id,
            active_player=True,
        )
    )
    card_instance: PlayerCardInstance = (
        await services.card_instance.get_card_instance_for_id(
            card_instanse_id=callback_data.id,
        )
    )
    logger.info("Получити card_instance с id - %s", card_instance.id)
    if not card_instance:
        logger.warning(
            "ошибка id - %s",
            callback_data.id,
        )
        raise GameError("Эта карта не находится у вас в сбросе 🛒")
    if card_instance.zone != CardZone.DISCARD:
        logger.warning("Неверная зона карты - %s", card_instance.zone)
        raise GameError("Эта карта уже не находится в сбросе. 🃏")
    await services.card_instance.change_zone_of_cards(
        card_instances=list(card_instance), card_zone=CardZone.HAND
    )
    photo = FSInputFile(media_dir / Path(card_instance.card.icon))
    await callback.message.answer_photo(
        photo=photo,
        caption=f"Вы выбрали карту {card_instance.card.name}",
    )
    services.session.commit()
