from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup

from app.backend.core.models.card import CardAction, CardEffect
from app.backend.core.models.game import Game
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.champion_move import ChampionService
from app.backend.crud.actions.destroy_card_move import DestroyCardService
from app.backend.crud.card_instance_crud import CardInstanceServices

from app.utils.logger import get_logger

if TYPE_CHECKING:
    from app.backend.core.models.play_card_instance import PlayerCardInstance


@dataclass
class EffectResult:
    action: CardAction
    instance: list[PlayerCardInstance]


class EffectExecutor:
    def __init__(
        self,
        session: AsyncSession,
        player_state: PlayerState,
        game: Game,
    ):
        self.session = session
        self.player_state = player_state
        self.game = game
        self.logger = get_logger(self.__class__.__name__)

    async def execute(self, effect: CardEffect):
        self.logger.info(
            "Эффект - %s, значение - %s",
            effect.action,
            effect.value,
        )

        method_name = (
            f"do_{effect.action}_"
            f"{effect.effect_type}_"
            f"{effect.condition_type}"
        )
        self.logger.info("method_name - %s", method_name)
        method = getattr(self, method_name, None)
        if method:
            return await method(
                value=effect.value,
                condition_value=effect.condition_value,
            )
        else:
            self.logger.error("Проблема нет такого effect")
            return None

    # ----------------------------- crystal ---------------------------------

    async def do_crystal_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        self.player_state.crystals += value
        self.logger.info(
            " функция - do_crystal_base_none, общее значение - %s",
            self.player_state.crystals,
        )

    async def do_crystal_conditional_mastery(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.mastery >= condition_value:
            self.player_state.crystals += value
        self.logger.info(
            " функция - do_crystal_conditional_mastery, значение - %s",
            self.player_state.crystals,
        )

    # ----------------------------- attack ---------------------------------

    async def do_attack_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        self.player_state.power += value

    async def do_attack_conditional_player_health(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.health == condition_value:
            self.player_state.power += value

    async def do_attack_conditional_mastery(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.mastery >= condition_value:
            self.player_state.power += value
        self.logger.info(
            " функция - do_attack_conditional_mastery, значение - %s",
            self.player_state.power,
        )

    async def do_attack_conditional_wilds_on_table(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.wilds_count >= condition_value:
            self.player_state.power += value
            self.logger.info(
                " функция - do_attack_conditional_card_on_table, значение - %s",
                self.player_state.power,
            )

    async def do_attack_conditional_player_health(
        self,
        value: int,
        condition_value: int,
    ):

        if self.player_state.health == condition_value:
            self.player_state.power += value

    # ----------------------------- healing ----------------------------------

    async def do_healing_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.health + value > 50:
            self.player_state.health = 50
        else:
            self.player_state.health += value
        self.logger.info(
            " функция - do_healing_base_none, значение - %s",
            self.player_state.health,
        )

    async def do_healing_conditional_wilds_on_table(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.wilds_count >= condition_value:
            if self.player_state.health + value > 50:
                self.player_state.health = 50
            else:
                self.player_state.health += value
        self.logger.info(
            " функция - do_healing_conditional_card_on_table, значение - %s",
            self.player_state.health,
        )

    async def do_healing_conditional_mastery(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.mastery == condition_value:
            self.player_state.health += value
            if self.player_state.health < 50:
                self.player_state.mastery = 50

    # ----------------------------- take_card ---------------------------------

    async def do_take_card_base_none(
        self,
        value: int,
        condition_value: int,
    ):

        self.logger.debug(
            "Начало do_take_card_base_none: запрошено %s карт, условие %s",
            value,
            condition_value,
        )
        card_instance_services = CardInstanceServices(session=self.session)
        await card_instance_services.take_card_to_hand(
            player_state=self.player_state,
            number_cards=value,
        )

    # ---------------------------------- might --------------------------------

    async def do_might_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.mastery == 30:
            pass
        else:
            self.player_state.mastery += value
            if self.player_state.mastery > 30:
                self.player_state.mastery = 30

    # ------------------------------- champion destroy ------------------------

    async def do_champion_destroy_conditional_wilds_on_table(
        self,
        value: int,
        condition_value: int,
    ):
        """Уничтожаем чемпиона врага."""

        if self.player_state.wilds_count >= condition_value:
            champion_service = ChampionService(session=self.session)
            champions: list[PlayerCardInstance] = (
                await champion_service.get_champions(
                    player_id=self.player_state.player_id
                )
            )

            if champions:
                self.logger.info("Получаем чемпионов - %s", champions)
                return EffectResult(
                    action=CardAction.CHAMPION_DESTROY, instance=champions
                )

            self.logger.info("Чемпионов нет - %s", champions)
        self.logger.info("Недостаточно карт wilds для зффекта")

    # ------------------------------- card_destroy ----------------------------

    async def do_card_destroy_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        """Удалить свою карту из руки или колоды."""

        destroy_service = DestroyCardService(session=self.session)
        cards: list[PlayerCardInstance] = destroy_service.get_card_for_destroy(
            game_id=self.game.id,
            player_state_id=self.player_state.id,
        )

        if cards:
            self.logger.info("Получаем карты - %s", cards)
            return EffectResult(
                action=CardAction.CARD_DESTROY,
                instance=cards,
            )

        self.logger.info("Карт нет - %s", cards)
