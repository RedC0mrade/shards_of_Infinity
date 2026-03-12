from pathlib import Path
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.play_card_instance import PlayerCardInstance
from app.backend.core.models.player_state import PlayerState
from app.telegram_bot.dependencies.dependencies import Services
from app.telegram_bot.keyboards.dmcc_keyboard import DestroyCardCallback
from app.utils.logger import get_logger


router = Router(name=__name__)
logger = get_logger(__name__)
media_dir = Path(__file__).parent.parent.parent.parent / "media"


@router.callback_query(DestroyCardCallback.filter())
async def handle_card_destroy(
    callback: CallbackQuery,
    callback_data: DestroyCardCallback,
    services: Services,
):
    await callback.message.edit_reply_markup(reply_markup=None)

    player_state: PlayerState = (
        await services.player_state.get_player_state_with_game(
            player_id=callback.from_user.id,
            active_player=True,
        )
    )
    logger.info("Получили player_state - %s", player_state)

    card_instance: PlayerCardInstance = await services.destroy.destroy_card(
        card_instance_id=callback_data.id
    )  # Рассмотреть вариант без destroy_card

    photo = FSInputFile(media_dir / Path(card_instance.card.icon))

    await callback.message.answer_photo(
        photo=photo,
        caption=f"Вы уничтожили свою карту карту: {card_instance.card.name}",
    )
    await callback.bot.send_photo(
        photo=photo,
        caption=f"Ваш противник уничтожил карту: {card_instance.card.name}",
        chat_id=player_state.game.non_active_player_id,
    )

    await services.session.commit()
