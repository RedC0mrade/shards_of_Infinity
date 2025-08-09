import secrets

from sqlalchemy import select
from app.backend.core.models.game import Game
from app.backend.core.models.user import TelegrammUser
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
async def handle_start(message: types.Message, command: CommandStart):
    """Команда старт."""
    async with db_helper.session_context() as session:
        user_data = UserCreateSchema(
            telegramm_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

        user_service = UserServices(session=session)
        user = await user_service.get_or_create_user(user_data)

        await message.answer(
            text=(
                f"Привет, {message.from_user.username}! "
                f"Твой ID: {user.telegramm_id}. "
                f"Твой Chat_id: {message.chat.id}"
            ),
            reply_markup=start_keyboard(),
        )


@router.message(F.text == StartKBText.START_GAME)
async def new_game(message: types.Message):
    invite_token = generate_invite_token()
    telegramm_id = message.from_user.id
    # game_data = CreateGameSchema(
    #     player1_id=player1_id,
    #     active_player_id=player1_id,
    #     invite_token=invite_token,
    # )

    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        user = await select(TelegrammUser).where(TelegrammUser.telegramm_id==telegramm_id)
        if not user:
        await game_service.create_game(game_data=game_data)

    await message.answer(
        text=(
        f"\U0001f3ae Игра создана!\n"
        f"🔗 Отправь этот токен другу для подключения:\n{invite_token}"
        )
    )
