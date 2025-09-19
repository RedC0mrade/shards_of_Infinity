from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.card import Card, CardFaction
from app.backend.core.models.player_state import PlayerState
from app.utils.logger import get_logger


class PlayStateExecutor:
    def __init__(
        self,
        session: AsyncSession,
        player_state: PlayerState,
    ):
        self.session = session
        self.player_state = player_state
        self.logger = get_logger(self.__class__.__name__)
        self.count_handlers: dict[CardFaction, callable] = {
            CardFaction.WILDS: self._inc_wilds,
            CardFaction.DEMIREALM: self._inc_demirealm,
            CardFaction.ORDER: self._inc_order,
            CardFaction.HOMODEUS: self._inc_homodeus,
        }

    async def faction_count(self, card: Card):
        """Увеличивает счетчик фракции у игрока"""
        self.logger.info("Начало функции faction_count")
        handler = self.count_handlers.get(card.faction, None)
        if not handler:
            self.logger.warning(
                "Нейтральная фракция %s у карты %s",
                card.faction,
                card.name,
            )
        await handler()

    async def _inc_wilds(self):
        self.player_state.wilds_count += 1
        self.logger.info(
            "Счетчик фракции wilds - %s", self.player_state.wilds_count
        )

    async def _inc_demirealm(self):
        self.player_state.demirealm_count += 1
        self.logger.info(
            "Счетчик фракции demirealm - %s", self.player_state.demirealm_count
        )

    async def _inc_order(self):
        self.player_state.order_count += 1
        self.logger.info(
            "Счетчик фракции order - %s", self.player_state.order_count
        )

    async def _inc_homodeus(self):
        self.player_state.homodeus_count += 1
        self.logger.info(
            "Счетчик фракции homodeus - %s", self.player_state.homodeus_count
        )
