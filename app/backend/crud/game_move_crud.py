import random
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card
from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.play_card_instance import PlayerCardInstance
from app.backend.core.models.player_state import PlayerState


class GameMove:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_market_cards(
        self,
        player_id: int,
        count: int,
    ):
        stmt = (
            select(Game)
            .join(PlayerState)
            .where(
                Game.status == GameStatus.IN_PROGRESS,
                PlayerState.player_id == player_id,
            )
        )
        result: Result = await self.session.execute(stmt)
        game: Game = result.scalar_one_or_none()
        if not game:
            raise ValueError("Игрок не участвует ни в одной игре")

        # 2. Все состояния игроков этой игры
        player_states_stmt = select(PlayerState).where(
            PlayerState.game_id == game.id
        )
        result: Result = await self.session.execute(player_states_stmt)
        player_states = result.scalars()
        player_states = list(player_states)

        # 3. Собираем id всех карт у игроков
        card_ids_stmt = select(PlayerCardInstance.card_id).where(
            PlayerCardInstance.player_state_id.in_(
                [ps.id for ps in player_states]
            )
        )
        result: Result = await self.session.execute(card_ids_stmt)
        player_card_ids = result.scalars()
        excluded_ids = set(player_card_ids)

        # 4. Все доступные карты, которых нет у игроков
        available_cards = await self.session.scalars(
            select(Card).where(Card.id.not_in(excluded_ids))
        )
        available_cards = tuple(available_cards)

        # 5. Выбираем случайные count карт
        if len(available_cards) < count:
            return available_cards

        return random.sample(available_cards, count)
