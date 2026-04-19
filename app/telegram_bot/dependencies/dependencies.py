from typing import Annotated, Any, Callable, Dict
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.crud.actions.attack_move import AttackServices
from app.backend.crud.actions.buy_move import BuyServices
from app.backend.crud.actions.champion_move import ChampionServices
from app.backend.crud.actions.defeat_move import DefeatService
from app.backend.crud.actions.destroy_card_move import DestroyCardServices

# from app.backend.crud.actions.game_move import MoveServices
from app.backend.crud.card_crud import CardServices
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.backend.crud.games_crud import GameServices
from app.backend.crud.hand_crud import HandServices
from app.backend.crud.market_crud1 import MarketServices
from app.backend.crud.player_state_crud import PlayerStateServices
from app.backend.crud.users_crud import UserServices
from app.backend.factories.database import db_helper


class Services:

    def __init__(self, session):
        self.session: AsyncSession = session
        self.card_instance = CardInstanceServices(session)
        self.card = CardServices(session)
        self.hand = HandServices(session)
        self.game = GameServices(session)
        self.champion = ChampionServices(session)
        self.player_state = PlayerStateServices(session)
        self.market = MarketServices(session)
        self.card_instance = CardInstanceServices(session)
        self.buy = BuyServices(session)
        self.destroy = DestroyCardServices(session)
        self.user = UserServices(session)
        # self.move = MoveServices(session, self.card_instance, self.card)
        self.attack = AttackServices(session, self.card_instance)
        self.defeat = DefeatService(session, self.user)


class DatabaseMiddleware(BaseMiddleware):

    async def __call__(
        self, handler: Callable, event, data: Dict[str, Any]
    ) -> Any:

        async with db_helper.session_context() as session:
            data["services"] = Services(session)
            return await handler(event, data)
