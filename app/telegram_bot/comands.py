import secrets
from app.backend.core.models.game import Game
from app.backend.crud.games import GameServices
from app.backend.factories.database import db_helper
from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from app.backend.crud.users_crud import UserServices
from app.backend.schemas.users import UserCreateSchema

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
            f"Привет, {user.first_name}! "
            f"Твой ID: {user.telegramm_id}. "
            f"Твой Chat_id: {message.chat.id}"
        )
    # if command.args and command.args.startswith("invite_"):
    #     token = command.args.replace("invite_", "")


def generate_invite_token():
    return secrets.token_hex(4)


@router.message(Command("newgame"))
async def new_game(message: types.Message):
    invite_token = generate_invite_token()
    player1_id = message.from_user.id
    bot_username = (await message.bot.me()).username
    invite_link = f"https://t.me/{bot_username}?start=invite_{invite_token}"
    async with db_helper.session_context() as session:
        came_service = GameServices(session=session)
        # game = Game(
        #     player1_id=player1_id,
        #     active_player_id=player1_id,
        #     invite_token=invite_token,
        # )

    await message.answer(
        f"\U0001f3ae Игра создана!\n"
        f"🔗 Отправь эту ссылку другу для подключения:\n{invite_link}"
    )
