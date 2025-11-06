from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logger import get_logger


class BaseService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)
