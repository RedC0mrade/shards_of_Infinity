from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup

from app.backend.core.models.card import (
    CardAction,
    CardEffect,
    CardFaction,
    CardType,
)
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import CardZone
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.actions.champion_move import ChampionService
from app.backend.crud.actions.destroy_card_move import DestroyCardService
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices

from app.backend.crud.market_crud1 import MarketServices
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

    async def do_crystal_conditional_champion_on_table(
        self,
        value: int,
        condition_value: int,
    ):
        self.logger.info(
            "Начало работы функции do_crystal_conditional_champion_on_table"
        )
        card_instance_service = CardInstanceServices(session=self.session)
        card_instance = card_instance_service.get_card_type_in_zone(
            game_id=self.game.id,
            player_state_id=self.player_state.id,
            zone=[CardZone.IN_PLAY],
            card_type=CardType.CHAMPION,
        )
        if len(card_instance) >= condition_value:
            self.player_state.crystals += value

    # ----------------------------- attack ---------------------------------

    async def do_attack_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        self.logger.info("Начало работы функции do_attack_base_none")
        self.player_state.power += value

    async def do_attack_conditional_player_health(
        self,
        value: int,
        condition_value: int,
    ):
        self.logger.info(
            "Начало работы функции do_attack_conditional_player_health"
        )
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

    async def do_attack_conditional_demirealm_in_reset(
        self,
        value: int,
        condition_value: int,
    ):
        card_instance_service = CardInstanceServices(session=self.session)
        instance = card_instance_service.get_faction_in_zone(
            game_id=self.game.id,
            player_state_id=self.player_state.id,
            zone=[CardZone.DISCARD],
            faction=CardFaction.DEMIREALM,
        )
        if len(instance) >= condition_value:
            self.player_state.power += value
            self.logger.info(
                " функция - do_attack_conditional_demirealm_in_reset, значение - %s",
                self.player_state.power,
            )

    async def do_attack_conditional_plus_two_for_each_demirealm_in_reset(
        self,
        value: int,
        condition_value: int,
    ):
        card_instance_service = CardInstanceServices(session=self.session)
        instance = card_instance_service.get_faction_in_zone(
            game_id=self.game.id,
            player_state_id=self.player_state.id,
            zone=[CardZone.DISCARD],
            faction=CardFaction.DEMIREALM,
        )
        self.player_state.power += 2 * len(instance)
        self.logger.info(
            " функция - do_attack_conditional_plus_two_for_each_demirealm_in_reset, значение - %s",
            self.player_state.power,
        )

    async def do_attack_conditional_player_health(
        self,
        value: int,
        condition_value: int,
    ):

        if self.player_state.health == condition_value:
            self.player_state.power += value

    async def do_attack_conditional_plus_value_for_each_homodeus_champion_in_game(
        self,
        value: int,
        condition_value: int,
    ):
        """Обработка карты Эвокатус"""

        self.logger.info(
            "Начало работы функции do_attack_conditional_plus_value_for_each_homodeus_champion_in_game"
        )
        card_instance_service = CardInstanceServices(session=self.session)
        instance = await card_instance_service.get_card_type_in_zone(
            game_id=self.game.id,
            player_state_id=self.player_state.id,
            zone=list(CardZone.IN_PLAY),
            card_type=CardType.CHAMPION,
        )
        if not instance:
            self.logger.info("нет чемпионов в игре")
        self.player_state.power = value * list(instance)
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

    async def do_take_card_conditional_mastery(
        self,
        value: int,
        condition_value: int,
    ):

        self.logger.debug(
            "Начало do_take_card_conditional_mastery: запрошено %s карт, условие - %s mastery - %s",
            value,
            condition_value,
            self.player_state,
        )

        if self.player_state.mastery >= condition_value:
            card_instance_services = CardInstanceServices(session=self.session)
            await card_instance_services.take_card_to_hand(
                player_state=self.player_state,
                number_cards=value,
            )

    # ------------------------------- take_mercenary ---------------------------

    async def do_take_mercenary_from_reset_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        """Добираем в руку наемника из сброса."""
        self.logger.info(" функция - do_take_mercenary_from_reset_base_none")
        card_instance_service = CardInstanceServices(session=self.session)
        instance = card_instance_service.get_card_type_in_zone(
            game_id=self.game.id,
            player_state_id=self.player_state.id,
            zone=[CardZone.DISCARD],
            card_type=CardType.MERCENARY,
        )
        if instance:
            self.logger.info("Получаем карты - %s", instance)
            return EffectResult(
                action=CardAction.TAKE_MERCENARY_FROM_RESET,
                instance=instance,
            )

        self.logger.info("Карт нет - %s", instance)

    # ---------------------------------- might --------------------------------

    async def do_might_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        self.logger.debug(
            "Начало do_might_base_none: value - %s, condition_value - %s",
            value,
            condition_value,
        )
        if self.player_state.mastery == 30:
            pass
        else:
            self.player_state.mastery += value
            if self.player_state.mastery > 30:
                self.player_state.mastery = 30

    async def do_might_conditional_wilds_homodeus_demirealm_on_table(
        self,
        value: int,
        condition_value: int,
    ):
        self.logger.debug(
            "Начало do_might_conditional_wilds_homodeus_demirealm_on_table: value - %s, condition_value - %s",
            value,
            condition_value,
        )
        card_service = CardServices(session=self.session)
        count = await card_service.card_order_check(
            player_state_id=self.player_state.id
        )
        if count and self.player_state.mastery < 30:
            self.player_state.mastery += value
            if self.player_state.mastery > 30:
                self.player_state.mastery = 30

    # ------------------------------- champion --------------------------------

    async def do_champion_destroy_conditional_wilds_on_table(
        self,
        value: int,
        condition_value: int,
    ):
        """Уничтожаем чемпиона врага."""

        self.logger.info(
            "Начало работы do_champion_destroy_conditional_wilds_on_table"
        )
        if self.player_state.wilds_count >= condition_value:
            champion_service = ChampionService(session=self.session)
            champions: list[PlayerCardInstance] = (
                await champion_service.get_champions(
                    player_id=self.player_state.player_id
                )
            )

            if champions:
                self.logger.info("Получаем id чемпионов - %s", champions)
                return EffectResult(
                    action=CardAction.CHAMPION_DESTROY,
                    instance=champions,
                )

            self.logger.info("Чемпионов нет - %s", champions)
        self.logger.info("Недостаточно карт wilds для зффекта")

    async def do_take_champion_from_reset_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        """Берем чемпиона из сброса"""

        self.logger.info(
            "Начало работы do_champion_destroy_conditional_wilds_on_table"
        )
        card_instance_service = CardInstanceServices(session=self.session)
        champions: list[PlayerCardInstance] = (
            card_instance_service.get_card_type_in_zone(
                game_id=self.game.id,
                player_state_id=self.player_state.id,
                zone=[CardZone.DISCARD],
                card_type=CardType.CHAMPION,
            )
        )
        if champions:
            self.logger.info("Получаем id чемпионов - %s", champions)
            return EffectResult(
                action=CardAction.TAKE_CHAMPION_FROM_RESET,
                instance=champions,
            )

        self.logger.info("Чемпионов нет - %s", champions)

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

    # ------------------------------- choose_card_from_market -----------------

    async def do_choose_card_from_market_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        """Выбрать карту с рынка, если могущества больше 15, взять в руку."""

        market_service = MarketServices(session=self.session)

        card_instance = await market_service.get_market_cards_less_six_cristals(
            game_id=Game.id
        )
        if card_instance:
            self.logger.info("Получаем состояния карт - %s", card_instance)
            return EffectResult(
                action=CardAction.CHOOSE_CARD_FROM_MARKET,
                instance=card_instance,
            )
