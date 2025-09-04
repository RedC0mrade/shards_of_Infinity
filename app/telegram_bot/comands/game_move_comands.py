from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.backend.core.models.card import Card
from app.backend.crud.card_crud import CardServices
from app.telegram_bot.keyboards.hand_keyboard import CallBackCard

from app.backend.factories.database import db_helper


router = Router(name=__name__)


@router.callback_query(CallBackCard.filter())
async def handle_play_card(
    callback: CallbackQuery,
    callback_data: CallBackCard,
):
    
    async with db_helper.session_context() as session:
        card_servises = CardServices(session=session)

        card: Card = await card_servises.get_card(card_id=callback_data.id)

        photo = FSInputFile(card.icon)

        
        await callback.message.answer_photo(
            photo=photo,
            caption=f"Карта {card.name} в вашей колоде"
        )
        # answer(text=f"Ты сыграл карту {id}, name {name}")
        await callback.from_user.id