from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardAction, EffectType
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.executors.effects_executor import EffectExecutor
from app.backend.crud.executors.ps_count_executor import PlayStateExecutor
from app.utils.logger import get_logger


class MoveServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def make_move(
        self,
        card: Card,
        game: Game,
        player_id: int,
        player_state: PlayerState,
        mercenary: bool = False,
    ) -> str:
        """Игрок разыгрывает карту."""

        self.logger.info(
            "Игрок с id - %s делает ход картой - %s, в игре с id - %s",
            player_id,
            card.name,
            game.id,
        )

        effect_executor = EffectExecutor(
            session=self.session,
            player_state=player_state,
            game=game,
        )

        for effect in card.effects:
            await effect_executor.execute(effect)  # Отрабатываем эффекты

        self.logger.info("Все эффекты обработаны. Переходим к faction_count")

        play_state_executor = PlayStateExecutor(
            session=self.session,
            player_state=player_state,
        )
        await play_state_executor.faction_count(
            card=card
        )  # Считаем разыранные карты
        self.logger.info(
            "faction_count отработала. Переходим к функции change_card_zone"
        )
        card_service = CardServices(session=self.session)
        
        start_zone = CardZone.MARKET if mercenary else CardZone.HAND
        answer = await card_service.change_card_zone(
            card_id=card.id,
            game_id=game.id,
            start_zone=start_zone,
            end_zone=CardZone.IN_PLAY,
        )
        if not answer[0]:
            self.logger.debug("Ошибка - текст ошибки: %s", answer[1])
            return answer[1]

        self.logger.info("Функция change_card_zone отработала. делаем commit")

        await self.session.commit()

# Розыгрыш карты:
# - Проверить есть ли карта в руке
# - Отыграть эффект
# - Обновить счетчик фрацкий сыграных в этом ходу
# - Поместить карту в сброс
