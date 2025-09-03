from sqlalchemy import Result, select
from app.backend.core.models.user import TelegramUser
from app.backend.crud.games_crud import GameServices
from app.backend.crud.hand_crud import HandServices
from app.backend.crud.market_crud1 import MarketServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.factories.database import db_helper
from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.backend.crud.users_crud import UserServices
from app.backend.schemas.games import CreateGameSchema
from app.backend.schemas.users import UserCreateSchema
from app.telegram_bot.keyboards.game_move_keyboard import in_play_card_keyboard
from app.telegram_bot.keyboards.start_keyboard import (
    start_keyboard,
    StartKBText,
)
from app.telegram_bot.stats.start_state import AcceptInvitationStates
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
                f"Привет, {user.first_name}!\n"
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
        stmt = select(TelegramUser).where(TelegramUser.id == chat_id)
        result: Result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            user_data = UserCreateSchema(
                chat_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )

            user_service = UserServices(session=session)
            user = await user_service.get_or_create_user(user_data)
        await game_service.create_game(game_data=game_data)

    await message.answer(
        text=(
            f"\U0001f3ae Игра создана!\n"
            f"🔗 Отправь этот токен другу для подключения:\n{invite_token}"
        )
    )


@router.message(F.text == StartKBText.ACCEPT_INVITATION)
async def ask_invite_code(message: types.Message, state: FSMContext):
    """Запрашиваем код приглашения у пользователя"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)

        # Проверяем, есть ли у пользователя активная игра
        if await game_service.has_active_game(player_id=message.from_user.id):
            await message.answer("❌ У вас уже есть активная игра.")
            return

    await message.answer("Введите код приглашения:")
    await state.set_state(AcceptInvitationStates.waiting_for_invite_code)


@router.message(AcceptInvitationStates.waiting_for_invite_code)
async def process_invite_code(message: types.Message, state: FSMContext):
    """Обрабатываем введённый код приглашения"""
    token = message.text.strip()
    player2_id = message.from_user.id

    async with db_helper.session_context() as session:
        get_player_state_service = PlayerStateServices(session=session)
        market_service = MarketServices(session=session)
        get_game_service = GameServices(session=session)
        hand_service = HandServices(session=session)
        game = await get_game_service.join_game_by_code(
            token=token,
            player2_id=player2_id,
        )
        if game:
            # Назначаем у кого сила 1, у кого 0
            player_states = get_player_state_service.assign_mastery(game=game)
            await get_player_state_service.create_play_state(
                play_datas=player_states
            )
            # Создаем мартет из 6 рандомных карт
            await market_service.create_market(game=game)

            await session.commit()

            # создаем стартовую руку у обоих пользователей
            await hand_service.create_hand(game.active_player_id)
            await hand_service.create_hand(game.non_active_player_id)

            await message.bot.send_message(
                chat_id=game.non_active_player_id,
                text="✅ Игра начинается, ходит ваш противник, удачи",
                reply_markup=in_play_card_keyboard(),
            )

            await message.bot.send_message(
                chat_id=game.active_player_id,
                text="✅ Игра начинается, ваш ход, удачи",
            )

        else:
            await message.answer(
                text="❌ Код приглашения не найден или игра уже началась.",
            )

    await state.clear()
