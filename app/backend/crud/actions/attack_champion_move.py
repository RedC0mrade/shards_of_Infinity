from sqlalchemy import Result, select
from app.backend.core.models.card import Card, CardType
from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.base_service import BaseService
from app.utils.exceptions.exceptions import ChampionError


class ChampionService(BaseService):

    async def attack_the_champion(
        card_instance_id: int,
        player_state: PlayerState,
    ):
        """Атака выбранного чемпиона."""
        pass

    async def get_champions(self, player_id: int) -> list[PlayerCardInstance]:
        """Получаем чемпионов противника в игре."""

        self.logger.info("Получаем чемпионов для игрока с id -%s", player_id)

        stmt = (
            select(PlayerCardInstance)
            .join(
                PlayerState,
                PlayerCardInstance.player_state_id == PlayerState.id,
            )
            .join(Card, Card.id == PlayerCardInstance.card_id)
            .join(Game, Game.id == PlayerCardInstance.game_id)
            .where(
                Game.status == GameStatus.IN_PROGRESS,
                Game.active_player_id == player_id,
                PlayerCardInstance.zone == CardZone.IN_PLAY,
                Card.card_type == CardType.CHAMPION,
                PlayerState.player_id == Game.non_active_player_id,
            )
        )

        result: Result = self.session.execute(stmt)
        cards_instance: list[PlayerCardInstance] = result.scalars().all()

        self.logger.info("cards_instance - %s", cards_instance)

        if not cards_instance:
            self.logger.info(
                "Игрок с id - %s, имеет чемпионов",
                player_id,
            )
            raise ChampionError(message="У противника нет чемпионов в игре")
        [
            self.logger.info(
                "Игрок с id - %s имеет чемпионов в игре - %s имеет чемпиона - %s",
                player_id,
                card_instance.game_id,
                card_instance.card.name,
            )
            for card_instance in cards_instance
        ]
        return cards_instance
