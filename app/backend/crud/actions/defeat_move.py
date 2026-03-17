from typing import TYPE_CHECKING

from app.backend.crud.base_service import BaseService
from app.backend.crud.users_crud import UserServices

if TYPE_CHECKING:
    from app.backend.core.models.game import Game, GameStatus
    from app.backend.core.models.user import TelegramUser

class DefeatService(BaseService):

    async def defeat(
        self,
        winner_id: int,
        loser_id: int,
        game: Game,
    ):
        """Регистрируем поражение."""
        user_service = UserServices(session=self.session)

        winner: TelegramUser = user_service.get_user_for_id(player_id=winner_id)
        loser: TelegramUser = user_service.get_user_for_id(player_id=loser_id)

        winner.victories += 1
        loser.defeats += 1
        game.status = GameStatus.FINISHED