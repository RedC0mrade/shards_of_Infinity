from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router(name=__name__)

@router.callback_query(F.data.startswith("play_card:"))
async def handle_play_card(callback: CallbackQuery):
    card_id = int(callback.data.split(":")[1])
    await callback.answer(text=f"Ты сыграл карту {card_id}")
