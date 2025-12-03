from sqlalchemy import Result, select
from app.backend.core.models.card import StartCardPlayer
from app.backend.core.models.game import Game
from app.backend.core.models.player_state import PlayerState
from app.backend.core.models.user import TelegramUser
from app.backend.crud.actions.game_move import MoveServices
from app.backend.crud.card_instance_crud import CardInstanceServices
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
from app.telegram_bot.keyboards.game_move_keyboard import (
    in_play_card_keyboard,
    non_play_card_keyboard,
)
from app.telegram_bot.keyboards.start_keyboard import (
    start_keyboard,
    StartKBText,
)
from app.telegram_bot.stats.start_state import AcceptInvitationStates
from app.utils.generate_token import generate_invite_token
from app.utils.logger import get_logger

router = Router(name=__name__)
logger = get_logger(__name__)


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
                f"Количество побед: {user.victories}\n"
                f"Количество поражений: {user.defeats}"
            ),
            reply_markup=start_keyboard(),
        )


@router.message(F.text == StartKBText.START_GAME)
async def new_game(message: types.Message):
    invite_token = generate_invite_token()

    game_data = CreateGameSchema(
        player1_id=message.from_user.id,
        active_player_id=message.from_user.id,
        invite_token=invite_token,
    )
    user_data = UserCreateSchema(
        chat_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        user_service = UserServices(session=session)
        await user_service.get_or_create_user(user_data)
        await game_service.create_game(game_data=game_data)

    await message.answer(
        text=(
            f"\U0001f3ae Игра создана!\n"
            f"🔗 Отправь этот токен другу для подключения:"
        )
    )
    await message.answer(text=f"{invite_token}")


@router.message(F.text == StartKBText.ACCEPT_INVITATION)
async def ask_invite_code(message: types.Message, state: FSMContext):
    """Запрашиваем код приглашения у пользователя"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)

        # Проверяем, есть ли у пользователя активная игра
        await game_service.has_active_game(player_id=message.from_user.id)

    await message.answer("Введите код приглашения:")
    await state.set_state(AcceptInvitationStates.waiting_for_invite_code)


@router.message(AcceptInvitationStates.waiting_for_invite_code)
async def process_invite_code(message: types.Message, state: FSMContext):
    """Обрабатываем введённый код приглашения"""
    token = message.text.strip()
    player2_id = message.from_user.id

    async with db_helper.session_context() as session:
        player_state_service = PlayerStateServices(session=session)
        market_service = MarketServices(session=session)
        game_service = GameServices(session=session)
        hand_service = HandServices(session=session)
        card_instance_service = CardInstanceServices(session=session)
        move_service = MoveServices(session=session)

        game = await game_service.join_game_by_code(
            token=token,
            player2_id=player2_id,
        )
        # Назначаем у кого сила 1, у кого 0
        player_states = player_state_service.assign_mastery(game=game)

        await player_state_service.create_play_state(
            play_data=player_states[0],
            game_id=game.id,
            player=StartCardPlayer.FIRST_PLAYER,
        )
        await player_state_service.create_play_state(
            play_data=player_states[1],
            game_id=game.id,
            player=StartCardPlayer.SECOND_PLAYER,
        )
        # Создаем маркет из 6 рандомных карт
        # await market_service.create_market(game=game)

        # создаем стартовую руку у обоих пользователей
        await hand_service.create_hand(game.active_player_id)
        await hand_service.create_hand(game.non_active_player_id)

        # создаем состояние для всех карт кроме стартовых
        await card_instance_service.create_card_instance_for_all_cards(
            game_id=game.id
        )

        await session.commit()
        logger.debug("No error 4")
        await message.bot.send_message(
            chat_id=game.non_active_player_id,
            text="🤖 Игра начинается, ходит ваш противник, удачи",
            reply_markup=non_play_card_keyboard(),
        )

        await message.bot.send_message(
            chat_id=game.active_player_id,
            text="✅ Игра начинается, ваш ход, удачи",
            reply_markup=in_play_card_keyboard(),
        )

    await state.clear()


@router.message(Command("play_keyboard"))
async def keyboard_return(message: types.Message):
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)

        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id
        )

        if game.active_player_id == message.from_user.id:
            await message.answer(
                text="Игровая клавиатура",
                reply_markup=in_play_card_keyboard(),
            )
            return
        elif game.non_active_player_id == message.from_user.id:
            await message.answer(
                text="Игровая клавиатура",
                reply_markup=non_play_card_keyboard(),
            )
            return
        return await message.answer(
            text="У вас нет активной партии",
        )
