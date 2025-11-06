from sqlalchemy import Result, select

from app.backend.crud.base_service import BaseService
from app.backend.core.models.user import TelegramUser
from app.backend.schemas.users import UserCreateSchema

class UserServices(BaseService):

    async def get_or_create_user(
        self,
        user_data: UserCreateSchema,
    ) -> TelegramUser:
        stmt = select(TelegramUser).where(TelegramUser.id == user_data.chat_id)
        result: Result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            self.logger.info("Пользователь уже существует - %s", user.username)
            return user
        self.logger.info("Новый пользователь")
        user = TelegramUser(
            **user_data.model_dump(),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        self.logger.info("Пользователь - %s", user.username)
        return user
