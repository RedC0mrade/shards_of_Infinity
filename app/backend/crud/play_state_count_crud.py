from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.player_state import PlayerState
from app.utils.logger import get_logger

class PlayStateExecutor:
    def __init__(
        self, player_state: PlayerState, session: AsyncSession
    ):
        self.player_state = player_state
        self.session = session
        self.logger = get_logger(self.__class__.__name__)
