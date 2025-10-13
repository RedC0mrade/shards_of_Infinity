from aiogram import Router, types, F
from aiogram.types import FSInputFile, InputMediaPhoto

from app.backend.core.models.game import Game
from app.backend.core.models.market import MarketSlot
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.games_crud import GameServices
from app.backend.crud.hand_crud import HandServices
from app.backend.crud.market_crud1 import MarketServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.factories.database import db_helper

from app.telegram_bot.keyboards.game_move_keyboard import MoveKBText
from app.telegram_bot.keyboards.hand_keyboard import make_card_move_keyboard

router = Router(name=__name__)


@router.message(F.text == MoveKBText.MARKET)
async def handle_market(message: types.Message):
    """Выводим рынок в порядке позиции"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        market_servise = MarketServices(session=session)
        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id
        )

        if not game:
            await message.answer("❌ У вас нет активной игры.")
            return

        market_cards: list[PlayerCardInstance] = (
            await market_servise.get_market_cards(game_id=game.id)
        )

        if not market_cards:
            await message.answer("❌ Нет карт на рынке.")
            return

        media = []  # переделать дублирующийся код
        for slot in market_cards:
            card = slot.card

            media.append(
                InputMediaPhoto(
                    media=FSInputFile(card.icon),
                )
            )

        await message.answer_media_group(media)
        await message.answer(
            text="Выберите карту для покупки",
            reply_markup=make_card_move_keyboard(
                instance_data=market_cards, market=True
            ),
        )


@router.message(
    F.text.in_(
        [
            MoveKBText.HAND,
            MoveKBText.CARDS_IN_PLAY,
            MoveKBText.PLAYER_DISCARD,
        ]
    )
)
async def handle_hand(message: types.Message):
    """Выводим карты в руке, на столе"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        hand_services = HandServices(session=session)
        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id
        )

        if not game:
            await message.answer("❌ У вас нет активной игры.")
            return

        if message.text == MoveKBText.HAND:
            hand_cards: list[PlayerCardInstance] = (
                await hand_services.get_cards_in_zone(
                    game_id=game.id,
                    card_zone=CardZone.HAND,
                    player_id=message.from_user.id,
                )
            )

        elif message.text == MoveKBText.CARDS_IN_PLAY:
            hand_cards: list[PlayerCardInstance] = (
                await hand_services.get_cards_in_play(
                    card_zone=CardZone.IN_PLAY,
                    game_id=game.id,
                )
            )

        elif message.text == MoveKBText.PLAYER_DISCARD:
            hand_cards: list[PlayerCardInstance] = (
                await hand_services.get_cards_in_zone(
                    game_id=game.id,
                    card_zone=CardZone.DISCARD,
                    player_id=message.from_user.id,
                )
            )

        if not hand_cards:
            await message.answer(f"❌ Нет карт.")
            return

        cards = []  # переделать дублирующийся код
        for slot in hand_cards:
            card = slot.card

            cards.append(
                InputMediaPhoto(
                    media=FSInputFile(card.icon),
                )
            )
        await message.answer_media_group(cards)
        if message.text == MoveKBText.HAND:

            await message.answer(
                "Выберите карту:",
                reply_markup=make_card_move_keyboard(
                    instance_data=hand_cards,
                ),
            )


@router.message(F.text == MoveKBText.GAME_PARAMETERS)
async def handle_game_parametrs(message: types.Message):
    """Выводим информацию о состояния игрока"""
    async with db_helper.session_context() as session:
        play_state_service = PlayerStateServices(session=session)

        play_state: PlayerState = (
            await play_state_service.get_player_state_with_game(
                player_id=message.from_user.id
            )
        )
        if not play_state:
            await message.answer("❌ У вас нет активной игры.")
            return

        if play_state.game.active_player_id == message.from_user.id:
            await message.answer(
                text=(
                    f"Здоровье ❤️ = {play_state.health}\n"
                    f"Мастерство ⚡ = {play_state.mastery}\n"
                    f"Кристалы = 💎 {play_state.crystals}\n"
                    f"Атака ⚔️ = {play_state.power}\n"
                    f"Разыграно карт фракции Ветвь 🌿 = {play_state.wilds_count}\n"
                    f"Разыграно карт фракции Порядок  ⚖️ = {play_state.order_count}\n"
                    f"Разыграно карт фракции Хомодеус 🤖 = {play_state.homodeus_count}\n"
                    f"Разыграно карт фракции Демириалм 👾= {play_state.demirealm_count}\n"
                )
            )
            return
        else:
            await message.answer(
                text=(
                    f"Здоровье ❤️ = {play_state.health}\n"
                    f"Мастерство ⚡ = {play_state.mastery}\n"
                    f"Щит 🛡️ = {play_state.shield}\n"
                )
            )


@router.message(F.text == MoveKBText.ENEMY_PARAMETERS)
async def enemy_game_parametrs(message: types.Message):
    """Выводим состояние противника"""

    async with db_helper.session_context() as session:
        play_state_service = PlayerStateServices(session=session)

        enemy_play_state: PlayerState = (
            await play_state_service.get_enemy_player_state_with_game(
                player_id=message.from_user.id
            )
        )
        if not enemy_play_state:
            await message.answer("❌ У вас нет активной игры.")
            return

        await message.answer(
            text=(
                f"Здоровье ❤️ = {enemy_play_state.health}\n"
                f"Мастерство ⚡ = {enemy_play_state.mastery}\n"
            )
        )
