from pathlib import Path
from aiogram import Router, types, F
from aiogram.types import FSInputFile, InputMediaPhoto

from app.backend.core.models.game import Game
from app.backend.core.models.market import MarketSlot
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.champion_move import ChampionService
from app.backend.crud.actions.attack_move import AttackService
from app.backend.crud.actions.defeat_move import DefeatService
from app.backend.crud.actions.game_move import MoveServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.games_crud import GameServices
from app.backend.crud.hand_crud import HandServices
from app.backend.crud.market_crud1 import MarketServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.crud.users_crud import UserServices
from app.backend.factories.database import db_helper


from app.telegram_bot.keyboards.dmcc_keyboard import KeyboardFactory
from app.telegram_bot.keyboards.game_move_keyboard import (
    MoveKBText,
    in_play_card_keyboard,
    non_play_card_keyboard,
)

from app.utils.exceptions.exceptions import GameError
from app.utils.logger import get_logger

router = Router(name=__name__)

media_dir = Path(__file__).parent.parent.parent.parent / "media"
logger = get_logger(__name__)


@router.message(F.text == MoveKBText.MARKET)
async def handle_market(message: types.Message):
    """Выводим рынок в порядке позиции"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        market_servise = MarketServices(session=session)
        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id
        )

        market_cards: list[PlayerCardInstance] = (
            await market_servise.get_market_cards(game_id=game.id)
        )

        media = []  # переделать дублирующийся код
        for slot in market_cards:
            card = slot.card
            icon_path = media_dir / Path(card.icon)
            logger.info("Путь до карты %s", icon_path)
            media.append(
                InputMediaPhoto(
                    media=FSInputFile(icon_path),
                )
            )
        await message.answer_media_group(media)

        if message.from_user.id == game.active_player_id:
            await message.answer(
                text="Выберите карту для покупки",
                reply_markup=KeyboardFactory.market(instance_data=market_cards),
            )


@router.message(
    F.text.in_(
        [
            MoveKBText.HAND,
            MoveKBText.PLAYER_DISCARD,
        ]
    )
)
async def handle_hand(message: types.Message):
    """Выводим карты в сбросе, на столе"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        hand_services = HandServices(session=session)
        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id
        )

        if message.text == MoveKBText.HAND:
            hand_cards: list[PlayerCardInstance] = (
                await hand_services.get_cards_in_zone(
                    game_id=game.id,
                    card_zone=CardZone.HAND,
                    player_id=message.from_user.id,
                )
            )

        else:
            hand_cards: list[PlayerCardInstance] = (
                await hand_services.get_cards_in_zone(
                    game_id=game.id,
                    card_zone=CardZone.DISCARD,
                    player_id=message.from_user.id,
                )
            )

        media = []  # переделать дублирующийся код
        logger.info("Карты для вывода ироку:")
        for slot in hand_cards:
            card = slot.card

            icon_path = media_dir / Path(card.icon)
            logger.info("--------------- %s", card.name)
            media.append(
                InputMediaPhoto(
                    media=FSInputFile(icon_path),
                )
            )
        if not media:
            logger.info("Карты отсутствуют")
            return await message.answer("❌ Нет карт")
        await message.answer_media_group(media)
        if message.text == MoveKBText.HAND:

            await message.answer(
                "Выберите карту:",
                reply_markup=KeyboardFactory.play_card(
                    instance_data=hand_cards,
                ),
            )


@router.message(F.text == MoveKBText.CARDS_IN_PLAY)
async def handle_cards_in_play(message: types.Message):
    """Выводим карты на столе"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        hand_service = HandServices(session=session)
        user_service = UserServices(session=session)
        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id
        )
        match message.from_user.id:
            case game.active_player_id:
                enemy_id = game.non_active_player_id
            case game.non_active_player_id:
                enemy_id = game.active_player_id

        hand_cards: list[PlayerCardInstance] = (
            await hand_service.get_cards_in_play(
                card_zone=CardZone.IN_PLAY,
                game_id=game.id,
                player_id=message.from_user.id,
            )
        )

        media = []  # переделать дублирующийся код
        for slot in hand_cards:
            card = slot.card

            icon_path = media_dir / Path(card.icon)
            logger.info("--------------- %s", card.name)
            media.append(
                InputMediaPhoto(
                    media=FSInputFile(icon_path),
                )
            )
        if not media:
            await message.answer(text="❌ Нет разыгранных карт")
        else:
            await message.answer(text="Карты разыгранные вами")
            await message.answer_media_group(media)

        hand_cards: list[PlayerCardInstance] = (
            await hand_service.get_cards_in_play(
                card_zone=CardZone.IN_PLAY,
                game_id=game.id,
                player_id=enemy_id,
            )
        )

        media = []  # переделать дублирующийся код
        for slot in hand_cards:
            card = slot.card

            icon_path = media_dir / Path(card.icon)
            logger.info("Путь до карты %s", icon_path)
            media.append(
                InputMediaPhoto(
                    media=FSInputFile(icon_path),
                )
            )
        if not media:
            await message.answer(
                text="❌ У противника нет разыгранных карт"
            )
        else:
            await message.answer(text="Карты разыгранные противником")
            await message.answer_media_group(media)


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
            # return
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
        player_state_service = PlayerStateServices(session=session)

        enemy_player_state: PlayerState = (
            await player_state_service.get_enemy_player_state_with_game(
                player_id=message.from_user.id
            )
        )

        await message.answer(
            text=(
                f"Здоровье ❤️ = {enemy_player_state.health}\n"
                f"Мастерство ⚡ = {enemy_player_state.mastery}\n"
                f"Щит 🛡️ = {enemy_player_state.shield}\n"
                f"Атака ⚔️ = {enemy_player_state.power}\n"
                f"Разыграно карт фракции Ветвь 🌿 = {enemy_player_state.wilds_count}\n"
                f"Разыграно карт фракции Порядок  ⚖️ = {enemy_player_state.order_count}\n"
                f"Разыграно карт фракции Хомодеус 🤖 = {enemy_player_state.homodeus_count}\n"
                f"Разыграно карт фракции Демириалм 👾= {enemy_player_state.demirealm_count}\n"
            )
        )


@router.message(F.text == MoveKBText.ATTACK_CHAMPION)
async def attack_enemy_champion(message: types.Message):
    """Атака чемпиона противника."""
    # 1) Получить всех чемпионов противника
    # 2) Выдать список для атаки
    async with db_helper.session_context() as session:

        champion_service = ChampionService(session=session)
        champions_card: list[PlayerCardInstance] = (
            await champion_service.get_champions(player_id=message.from_user.id)
        )
        if champions_card:
            media = []  # переделать дублирующийся код
            for champion in champions_card:
                card = champion.card

                icon_path = media_dir / Path(card.icon)
                logger.info("--------------- %s", card.name)
                media.append(
                    InputMediaPhoto(
                        media=FSInputFile(icon_path),
                    )
                )
            await message.answer_media_group(media=media)
            await message.answer(
                text="Выберите Чемпиона для Атаки",
                reply_markup=KeyboardFactory.attack_champion(
                    instance_data=champions_card,
                ),
            )


@router.message(F.text == MoveKBText.ATTACK)
async def attack_enemy_player(message: types.Message):
    """Атака противника."""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        player_state_service = PlayerStateServices(session=session)
        attack_service = AttackService(session=session)

        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id,
            active_player=True,
        )

        enemy_state: PlayerState = (
            await player_state_service.get_player_state_with_game(
                player_id=game.non_active_player_id,
            )
        )
        player_state: PlayerState = (
            await player_state_service.get_player_state_with_game(
                player_id=message.from_user.id,
                active_player=True,
            )
        )
        attack = player_state.power
        attack_service = await attack_service.attack(
            player_state=player_state,
            enemy_state=enemy_state,
        )
        await message.answer(
            text=(
                f"Вы нанесли противнику ⚔️{attack} урона\nОсталось "
                f"здоровья 💚{enemy_state.health}"
            )
        )
        await message.bot.send_message(
            text=(
                f"Ваш противник нанес ⚔️{attack} урона\nОсталось "
                f"здоровья 💚{enemy_state.health}"
            ),
            chat_id=game.non_active_player_id,
        )


@router.message(F.text == MoveKBText.END)
async def end_move(message: types.Message):
    """Конец хода."""
    async with db_helper.session_context() as session:
        move_service = MoveServices(session=session)
        player_state_service = PlayerStateServices(session=session)

        player_state: PlayerState = (
            await player_state_service.get_player_state_with_game(
                player_id=message.from_user.id,
                active_player=True,
            )
        )
        emeny_state: PlayerState = (
            await player_state_service.get_enemy_player_state_with_game(
                player_id=player_state.player_id
            )
        )
        logger.critical(
            "id player_state игрока - %s, id игры - %s",
            player_state.id,
            player_state.game.id,
        )
        await move_service.pre_make_move(
            player_state=emeny_state,
            game=player_state.game,
        )
        logger.critical(
            "id player_state игрока - %s, id игры - %s перед after_the_move",
            player_state.id,
            player_state.game.id,
        )
        await move_service.after_the_move(
            player_state=player_state,
            game=player_state.game,
        )
        # await session.commit()

        await message.answer(
            text="Ваш ход окончен. Ходит Ваш противник",
            reply_markup=non_play_card_keyboard(),
        )  # Прикрепить клавиатуру не активного игорька

        await message.bot.send_message(
            text="Ваш ход!",
            chat_id=player_state.game.active_player_id,
            reply_markup=in_play_card_keyboard(),
        )
        await session.commit()


@router.message(F.text == MoveKBText.MASTERY)
async def get_concentration(message: types.Message):
    """Добавление +1 к мастерству."""
    async with db_helper.session_context() as session:
        player_state_service = PlayerStateServices(session=session)
        move_service = MoveServices(session=session)

        player_state: PlayerState = (
            await player_state_service.get_player_state_with_game(
                player_id=message.from_user.id,
                active_player=True,
            )
        )

        change_player_state: PlayerState = await move_service.get_mastery(
            player_state=player_state
        )
        await message.answer(
            text=(f"Мастерство ⚡ теперь равно = {change_player_state.mastery}")
        )
