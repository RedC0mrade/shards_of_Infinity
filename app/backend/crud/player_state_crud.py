import random
from typing import TYPE_CHECKING
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.schemas.play_state import CreatePlayStateSchema
from app.utils.logger import get_logger

if TYPE_CHECKING:
    from app.backend.core.models.game import Game


class PlayerStateServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def create_play_state(
        self,
        play_datas: list[CreatePlayStateSchema],
    ) -> list[PlayerState]:
        self.logger.info(
            "Создание play_state для игроков: %s",
            [p.player_id for p in play_datas],
        )
        stmt = select(Card.id).where(Card.start_card == True)
        result = await self.session.execute(stmt)
        start_card_ids: list[int] = result.scalars().all()

        if not start_card_ids:
            raise ValueError("В базе нет стартовых карт!")

        play_states = [
            PlayerState(
                **play_data.model_dump(),
                cards=[
                    PlayerCardInstance(
                        card_id=card_id,
                        zone=CardZone.DECK,
                    )
                    for card_id in start_card_ids
                ]
            )
            for play_data in play_datas
        ]
        self.session.add_all(play_states)
        await self.session.flush()  # Не забыть, что нужно закоммитить
        self.logger.info(
            "Создано play_state: %s", [ps.player_id for ps in play_states]
        )
        return play_states

    def assign_mastery(self, game: Game) -> list[CreatePlayStateSchema]:
        """Назначает mastery игрокам в зависимости от того, чей ход первый."""
        player1_id = game.player1_id
        player2_id = game.player2_id

        self.logger.info("Назначение mastery для игры %s", game.id)

        if game.active_player_id == player1_id:
            res = [
                CreatePlayStateSchema(
                    game_id=game.id, player_id=player1_id, mastery=0
                ),
                CreatePlayStateSchema(
                    game_id=game.id, player_id=player2_id, mastery=1
                ),
            ]
        else:
            res = [
                CreatePlayStateSchema(
                    game_id=game.id, player_id=player1_id, mastery=1
                ),
                CreatePlayStateSchema(
                    game_id=game.id, player_id=player2_id, mastery=0
                ),
            ]

        self.logger.info(
            "Mastery назначено: %s", {r.player_id: r.mastery for r in res}
        )
        return res

    async def draw_cards(
        self,
        player_state: PlayerState,
        count: int = 5,
    ) -> list[PlayerCardInstance]:
        """Добор карт в руку"""
        # 1. Сколько карт уже в руке
        current_hand = [
            c for c in player_state.cards if c.zone == CardZone.HAND
        ]
        need_to_draw = count - len(current_hand)
        if need_to_draw <= 0:
            return current_hand

        drawn_cards: list[PlayerCardInstance] = []

        while need_to_draw > 0:
            # Берём карты из DECK
            deck_cards = [
                c for c in player_state.cards if c.zone == CardZone.DECK
            ]
            if not deck_cards:
                # Если DECK пуст — перемешиваем DISCARD обратно в DECK
                discard_cards = [
                    c for c in player_state.cards if c.zone == CardZone.DISCARD
                ]
                if not discard_cards:
                    break  # вообще нет карт
                # Перемещаем в DECK
                for c in discard_cards:
                    c.zone = CardZone.DECK
                random.shuffle(discard_cards)  # перемешивание
                # можно обновить order_in_zone
                for idx, c in enumerate(discard_cards):
                    c.order_in_zone = idx

                deck_cards = discard_cards

            # Добираем одну карту
            card = deck_cards.pop(0)  # верхняя
            card.zone = CardZone.HAND
            drawn_cards.append(card)
            need_to_draw -= 1

        return drawn_cards

    async def get_game(self, player_id: int) -> Game:

        stmt = (
            select(PlayerState)
            .options(joinedload(PlayerState.game))
            .where(PlayerState.player_id == player_id)
        )
        result: Result = self.session.execute(stmt)
        player_state = result.scalar_one_or_none()

        return player_state
