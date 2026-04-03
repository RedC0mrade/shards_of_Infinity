from app.backend.crud.base_service import BaseService
from app.backend.crud.users_crud import UserServices

from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.user import TelegramUser


class DefeatService(BaseService):

    def __init__(self, session, user_service):
        super().__init__(session)
        self.user = user_service

    async def defeat(
        self,
        winner_id: int,
        loser_id: int,
        game: Game,
    ):
        """Регистрируем поражение."""

        winner: TelegramUser = self.user.get_user_for_id(player_id=winner_id)
        loser: TelegramUser = self.user.get_user_for_id(player_id=loser_id)

        winner.victories += 1
        loser.defeats += 1
        game.status = GameStatus.FINISHED
