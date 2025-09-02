from aiogram import Router, types, F
from aiogram.types import FSInputFile, InputMediaPhoto

from app.backend.core.models.game import Game
from app.backend.core.models.market import MarketSlot
from app.backend.core.models.play_card_instance import PlayerCardInstance
from app.backend.crud.games_crud import GameServices
from app.backend.crud.hand_crud import HandServices
from app.backend.crud.market_crud1 import MarketServices
from app.backend.factories.database import db_helper

from app.telegram_bot.keyboards.game_move_keyboard import MoveKBText

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

        market_slots: list[MarketSlot] = await market_servise.get_market_slots(
            game_id=game.id
        )

        if not market_slots:
            await message.answer("❌ Нет карт на рынке.")
            return

        media = []  # переделать дублирующийся код
        for slot in market_slots:
            card = slot.card

            media.append(
                InputMediaPhoto(
                    media=FSInputFile(card.icon),
                )
            )

        await message.answer_media_group(media)


@router.message(F.text == MoveKBText.HAND)
async def handle_hand(message: types.Message):
    """Выводим карты в руке"""
    async with db_helper.session_context() as session:
        game_service = GameServices(session=session)
        hand_services = HandServices(session=session)
        game: Game = await game_service.get_active_game(
            player_id=message.from_user.id
        )

        if not game:
            await message.answer("❌ У вас нет активной игры.")
            return

        hand_cards: list[PlayerCardInstance] = await hand_services.create_hand(
            player_id=message.from_user.id
        )

        if not hand_cards:
            await message.answer("❌ Нет карт в руке.")
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
