from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from app.keyboards.survey_keyboard import build_yes_or_no_kb
from app.routers.survey.states import Survey
from app.routers.validators.email_validator import valid_email_filter


router = Router(name=__name__)


@router.message(Command("survey", prefix="!/"))
async def handel_start_survey(
    message: types.Message,
    state: FSMContext,
):
    await state.set_state(Survey.full_name)
    await message.answer("Welcome to our weekly survey. What's your name?")


@router.message(
    Survey.full_name, F.text
)  # обрабатываем, что бы ответ был текст
async def handle_servey_user_full_name(
    message: types.Message,
    state: FSMContext,
):
    await state.update_data(full_name=message.text)  # Сохраняем состояние
    # await state.clear()                           # Очишаем состояние
    await state.set_state(Survey.email)
    await message.answer(
        text=f"Hellow {markdown.hbold(message.text)}, what's your email?",
        reply_markup=types.ReplyKeyboardRemove(), # Сбрасываем клавиатуру, если вдруг что осталось
    )


@router.message(
    Survey.email, valid_email_filter
)  # обрабатываем, что адрес корректный
async def handle_servey_user_email(
    message: types.Message,
    state: FSMContext,
    email: str,
):
    await state.update_data(email=message.text)  # Сохраняем состояние
    await state.get_state(Survey.email_newsletter)
    await message.answer(
        text=(
            f"Your email {markdown.hbold(email)}."
            " Would you like to be contacted in future?"
        ),
        reply_markup=build_yes_or_no_kb(),
    )


@router.message(Survey.email_newsletter, F.text.casefold() == "Yes")
async def handel_servey_email_newslettr_yes(
    message: types.Message,
    state: FSMContext,
):
    message.answer(
    )


@router.message(
    Survey.full_name
)  # обрабатываем не корректный ответ, если это не текст, а что то другое
async def handle_servey_user_full_name_invalid_content_type(
    message: types.Message,
):
    await message.answer(
        text=f"Wrong message type, send your name as text",
    )


@router.message(
    Survey.email
)  # обрабатываем не корректный ответ, если это не текст, а что то другое
async def handle_servey_user_email_invalid(
    message: types.Message,
):
    await message.answer(
        text=f"invalid email",
    )
