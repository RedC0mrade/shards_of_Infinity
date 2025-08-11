import secrets

from sqlalchemy import Result, select
from app.backend.core.models.game import Game
from app.backend.core.models.user import TelegramUser
from app.backend.crud.games_crud import GameServices
from app.backend.factories.database import db_helper
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from app.backend.crud.users_crud import UserServices
from app.backend.schemas.games import CreateGameSchema
from app.backend.schemas.users import UserCreateSchema
from app.telegram_bot.keyboards.start_keyboard import (
    start_keyboard,
    StartKBText,
)
from app.utils.generate_token import generate_invite_token

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    """Команда старт."""
    async with db_helper.session_context() as session:
        user_data = UserCreateSchema(
            chat_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

        user_service = UserServices(session=session)
        user = await user_service.get_or_create_user(user_data)

        await message.answer(
            text=(
                f"Привет, {user.username}!\n"
                f"Твой ID: {user.id}.\n"
                f"Твой Chat_id: {user.chat_id}\n"
                f"Количество побед: {user.victories}\n"
                f"Количество поражений: {user.defeats}"
            ),
            reply_markup=start_keyboard(),
        )


@router.message(F.text == StartKBText.START_GAME)
async def new_game(message: types.Message):
    invite_token = generate_invite_token()
    chat_id = message.from_user.id
    game_data = CreateGameSchema(
        player1_id=chat_id,
        active_player_id=chat_id,
        invite_token=invite_token,
    )

    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        stmt = select(TelegramUser).where(TelegramUser.id==chat_id)
        result: Result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        # if not user:
        await game_service.create_game(game_data=game_data)

    await message.answer(
        text=(
        f"\U0001f3ae Игра создана!\n"
        f"🔗 Отправь этот токен другу для подключения:\n{invite_token}"
        )
    )
