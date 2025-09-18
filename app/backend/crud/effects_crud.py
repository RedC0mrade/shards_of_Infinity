from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import CardEffect
from app.backend.core.models.game import Game
from app.backend.core.models.player_state import PlayerState
from app.utils.logger import get_logger


class EffectExecutor:
    def __init__(
        self, player_state: PlayerState, game: Game, session: AsyncSession
    ):
        self.player_state = player_state
        self.game = game
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def execute(self, effect: CardEffect):
        self.logger.info("Эффект %s", effect)
        method_name = (
            f"do_{effect.action.name.lower()}_"
            f"{effect.effect_type.name.lower()}_"
            f"{effect.condition_type.name.lower()}"
        )
        self.logger.info("method_name %s", method_name)
        method = getattr(self, method_name, None)
        if method:
            await method(
                value=effect.value,
                condition_value=effect.condition_value,
            )
        else:
            self.logger.error("Проблема с effect")

    async def do_crystal_base_none(
        self,
        value: int,
        condition_value: int,
    ):
        self.player_state.crystals += value
        self.logger.info(
            "do_crystal_base_none %s",
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
            "do_crystal_conditional_mastery %s",
            self.player_state.crystals,
        )

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
            "do_attack_conditional_mastery %s",
            self.player_state.power,
        )

    async def do_attack_conditional_card_on_table(
        self,
        value: int,
        condition_value: int,
    ):
        if self.player_state.wilds_count >= condition_value:
            self.player_state.power += value
        self.logger.info(
            "do_attack_conditional_card_on_table %s",
            self.player_state.power,
        )

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
            "do_healing_base_none %s",
            self.player_state.health,
        )

    async def do_healing_conditional_card_on_table(
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
            "do_healing_conditional_card_on_table %s",
            self.player_state.health,
        )
