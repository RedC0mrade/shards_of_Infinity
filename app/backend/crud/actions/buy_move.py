from random import choice
from sqlalchemy import Result, select
from typing import TYPE_CHECKING


from app.backend.crud.base_service import BaseService
from app.utils.exceptions.exceptions import InvalidCardZone, NotEnoughCrystals
from app.backend.core.models.player_state import PlayerState
from app.backend.core.models.card import Card
from app.backend.core.models.game import Game
from app.backend.core.models.play_card_instance import (
    CardZone,
    PlayerCardInstance,
)



class BuyServices(BaseService):

    async def buy_card_from_market(
        self,
        player_state: PlayerState,
        card: Card,
        card_instance: PlayerCardInstance,
        game: Game,
        player_id: int,
    ) -> tuple[bool, str]:
        """Игрок покупает карту с рынка."""

        self.logger.info(
            "Игрок id - %s покупает карту - %s, в игре id - %s, зоне - %s",
            player_id,
            card.name,
            game.id,
            card_instance.zone,
        )
        if player_state.crystals < card.crystals_cost:
            self.logger.warning(
                "Недостаточно кристалов (%s), для покупки необходимо - %s",
                player_state.crystals,
                card.crystals_cost,
            )
            raise NotEnoughCrystals(
                f"Недостаточно кристаллов💎 — у вас {player_state.crystals}, "
                f"а карта 🃏 {card.name} стоит {card.crystals_cost}💎."
            )

        if card_instance.zone != CardZone.MARKET:
            self.logger.warning(
                "Не правильная зона карты %s",
                card_instance.zone,
            )
            raise InvalidCardZone("Эта карта уже не находится на рынке 🃏.")

        player_state.crystals -= card.crystals_cost
        self.logger.info(
            "оставщееся количество кристалов - %s",
            player_state.crystals,
        )
        card_instance.zone = CardZone.DISCARD
        card_instance.player_state_id = player_state.id
        position_on_market = card_instance.position_on_market
        card_instance.position_on_market = None

        await self.replacement_cards_from_the_market(
            game_id=game.id,
            position_on_market=position_on_market,
        )

        await self.session.commit()
        self.logger.info(
            "Игрок %s успешно купил карту '%s' (новое состояние рынка обновлено)",
            player_id,
            card.name,
        )

    async def replacement_cards_from_the_market(  # Может стоит здесь передавать id карты которую хотим поменять и менять ее на None и присваивать id игорька?
        self,
        game_id: int,
        position_on_market: int,
    ):
        "Заменяем карту купленную с рынка."
        self.logger.info(
            "Делаем замену карты на рынке position_on_market - %s",
            position_on_market,
        )
        stmt = select(PlayerCardInstance).where(
            PlayerCardInstance.game_id == game_id,
            PlayerCardInstance.zone == CardZone.COMMON_DECK,
        )
        result: Result = await self.session.execute(stmt)
        available_cards_instance_id = result.unique().scalars().all()
        self.logger.info(
            "Получаем id состояния карты в общей колоде, всего карт - %s",
            len(available_cards_instance_id),
        )
        if not available_cards_instance_id:
            self.logger.error(
                "Нет доступных состояний карт для рынка в игре %s",
                game_id,
            )
            return []

        replacement_card_instance: PlayerCardInstance = choice(
            available_cards_instance_id
        )
        self.logger.info(
            "Получаем id состояния карты на замену - %s, position_on_market - %s",
            replacement_card_instance.id,
            position_on_market,
        )

        replacement_card_instance.position_on_market = position_on_market
        replacement_card_instance.zone = CardZone.MARKET

        self.logger.info(
            "replacement_card_instance.position_on_market - %s, position_on_market - %s",
            replacement_card_instance.position_on_market,
            position_on_market,
        )
        self.logger.info("Выполняем коммит")
        # await self.session.commit() # Нужен ли здесь комит???
