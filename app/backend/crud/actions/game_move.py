from sqlalchemy import Result, delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import (
    Card,
    CardAction,
    CardFaction,
    EffectType,
)
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.base_service import BaseService
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.executors.effects_executor import EffectExecutor
from app.backend.crud.executors.ps_count_executor import PlayStateExecutor
from app.backend.crud.hand_crud import HandServices
from app.utils.exceptions.exceptions import (
    ConcentrationError,
    NotEnoughCrystals,
)
from app.utils.logger import get_logger


class MoveServices(BaseService):

    async def pre_make_move(
        self,
        player_state: PlayerState,
        game: Game,
    ):
        # Что необходимо сделать перед ходом
        # 1) Обнулить все показатели. Атаки, защиты, щита
        # 2) Обновить обновить счетчик фракций
        self.logger.info(
            "Состояние player_state на начало функции,\n ---power - %s,\n ---shild - %s,\n ---crystals - %s,\n ---wilds - %s,\n ---homodeus - %s,\n ---order - %s,\n ---demirealm - %s,\n ---nconcentration -%s",
            player_state.power,
            player_state.shield,
            player_state.crystals,
            player_state.wilds_count,
            player_state.homodeus_count,
            player_state.order_count,
            player_state.demirealm_count,
            player_state.concentration,
        )
        self.logger.warning(
            "Game id - %s",
            game.id,
        )
        player_state.power = 0
        player_state.shield = 0
        player_state.crystals = 0
        player_state.concentration = False

        stmt = (
            select(Card.faction, func.count())
            .join(PlayerCardInstance, PlayerCardInstance.card_id == Card.id)
            .where(
                PlayerCardInstance.zone == CardZone.IN_PLAY,
                PlayerCardInstance.game_id == game.id,
                PlayerCardInstance.player_state_id == player_state.id,
            )
            .group_by(Card.faction)
        )
        result: Result = await self.session.execute(stmt)
        faction_counts = dict(result.all())

        player_state.wilds_count = faction_counts.get(
            CardFaction.WILDS,
            0,
        )
        player_state.order_count = faction_counts.get(
            CardFaction.ORDER,
            0,
        )
        player_state.homodeus_count = faction_counts.get(
            CardFaction.HOMODEUS,
            0,
        )
        player_state.demirealm_count = faction_counts.get(
            CardFaction.DEMIREALM,
            0,
        )
        self.logger.info(
            "Состояние player_state на конец функции,\n +++power - %s,\n +++shild - %s,\n +++crystals - %s,\n +++wilds - %s,\n +++homodeus - %s,\n +++order - %s,\n +++demirealm - %s,\n +++nconcentration -%s",
            player_state.power,
            player_state.shield,
            player_state.crystals,
            player_state.wilds_count,
            player_state.homodeus_count,
            player_state.order_count,
            player_state.demirealm_count,
            player_state.concentration,
        )
        await self.session.flush()  # закомитится в хендлере

    async def make_move(
        self,
        card: Card,
        game: Game,
        player_id: int,
        player_state: PlayerState,
        mercenary: bool = False,
    ) -> str:
        """Игрок разыгрывает карту."""
        # Розыгрыш карты:
        # - Проверить есть ли карта в руке
        # - Отыграть эффект
        # - Обновить счетчик фрацкий сыграных в этом ходу
        # - Поместить карту в сброс
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
        await card_service.change_card_zone(
            card_id=card.id,
            game_id=game.id,
            start_zone=start_zone,
            end_zone=CardZone.IN_PLAY,
        )

        self.logger.info("Функция change_card_zone отработала. делаем commit")

        await self.session.commit()

    async def after_the_move(
        self,
        player_state: PlayerState,
        game: Game,
    ):
        """Действия после окончания хода"""

        # 0) Поменять активного и не активного игрока местами
        # 1) Сбросить все карты из руки и на столе, кроме чемпионов
        # 2) Набрать новые карты
        # 3) Посчитать щиты

        card_instance_service = CardInstanceServices(session=self.session)
        hand_service = HandServices(session=self.session)
        self.logger.info(
            "Активный позльзователь - %s, не активный - %s",
            game.active_player_id,
            game.non_active_player_id,
        )
        self.logger.warning(
            "Game id в after_the_move - %s",
            game.id,
        )
        game.active_player_id, game.non_active_player_id = (
            game.non_active_player_id,
            game.active_player_id,
        )  # не забыть что нужно закоммитить

        cards_intances = (
            await card_instance_service.get_player_cards_instance_in_play(
                player_state=player_state,
            )
        )
        self.logger.info(
            "отработала card_instance_service.get_player_cards_instance_in_play, результат - %s",
            cards_intances,
        )
        if cards_intances:
            self.logger.info("Разыгранные карты:")
            for instace in cards_intances:
                self.logger.info("  - %s", instace.card.name)
            await card_instance_service.change_zone_of_cards(
                card_instances=cards_intances,
            )  # не забыть что нужно закоммитить

        hand: list[PlayerCardInstance] = await hand_service.create_hand(
            player_id=player_state.player_id,
        )

        player_state.shield = sum(
            [card_instance.card.shield for card_instance in hand]
        )
        self.logger.info("щит равен - %s", player_state.shield)

        await self.session.flush()

        self.logger.info(
            "Активный позльзователь - %s, не активный - %s",
            game.active_player_id,
            game.non_active_player_id,
        )

    async def get_mastery(
        self,
        player_state: PlayerState,
    ):
        if player_state.crystals == 0:
            raise NotEnoughCrystals(
                "Нет достаточно кристалов для концентрации"
            )
        if player_state.concentration == True:
            raise ConcentrationError(
                "Вы уже использовали концентрацию в этот ход"
            )
        if player_state.mastery >= 30:
            player_state.concentration = 30
            raise ConcentrationError(
                "Достигнуто максимальное количество могущества"
            )
        player_state.concentration = True
        player_state.concentration += 1
        player_state.crystals -= 1

        self.session.commit()