from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import CardEffect
from app.backend.core.models.game import Game
from app.backend.core.models.player_state import PlayerState
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.utils.logger import get_logger


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
        self.logger.info("Эффект %s", effect.action)

        method_name = (
            f"do_{effect.action}_"
            f"{effect.effect_type}_"
            f"{effect.condition_type}"
        )
        self.logger.info("method_name - %s", method_name)
        method = getattr(self, method_name, None)
        if method:
            await method(
                value=effect.value,
                condition_value=effect.condition_value,
            )
        else:
            self.logger.error("Проблема с effect")

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

    # ----------------------------- healing ---------------------------------

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

    # ----------------------------- take_card ---------------------------------

    async def do_take_card_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        card_instance_services = CardInstanceServices(session=self.session)
        await card_instance_services.take_card_to_hand(
            player_state=self.player_state,
            number_cards=value,
        )
