from aiogram import Router, types
from aiogram.filters import Command


router = Router(name=__name__)

@router.message(Command("survey", prefix="!/"))
async def handel_start_survey(message: types.Message):
    await message.answer(
        "Welcome to our weekly survey. What's your name?"
    )