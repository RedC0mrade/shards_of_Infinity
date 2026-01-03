from sqlalchemy import Result, and_, or_, select

from app.backend.core.models.game import Game, GameStatus
from app.backend.crud.base_service import BaseService
from app.backend.core.models.user import TelegramUser
from app.backend.schemas.users import UserCreateSchema
from app.utils.exceptions.exceptions import WrongUserId


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

    async def get_user_for_id(self, player_id: int) -> TelegramUser:
        """Получаем пользователя по id."""

        self.logger.info("Получаем пользователя по id - %s")
        stmt = select(TelegramUser).where(TelegramUser.id == player_id)
        result: Result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            self.logger.info(
                "Пользователь с id - %s, не найден",
                player_id,
            )
            raise WrongUserId(message="Ошибка пользователя")
        return user

    async def get_enemy(self, player_id: int, game_id: int):
        """Получаем id противника."""

        self.logger.info(
            "Получаем id противника(%s) в игре - %s",
            player_id,
            game_id,
        )
        stmt = (
            select(TelegramUser.id)
            .join(
                Game,
                or_(
                    Game.active_player_id == TelegramUser.id,
                    Game.non_active_player_id == TelegramUser.id,
                ),
            )
            .where(
                Game.id == game_id,
                Game.status == GameStatus.IN_PROGRESS,
                TelegramUser.id != player_id,
                or_(
                    and_(
                        Game.active_player_id == player_id,
                        Game.non_active_player_id == TelegramUser.id,
                    ),
                    and_(
                        Game.non_active_player_id == player_id,
                        Game.active_player_id == TelegramUser.id,
                    ),
                ),
            )
        )
        result: Result = await self.session.execute(stmt)
        enemy_id = result.scalar_one_or_none()
        if not enemy_id:
            self.logger.info(
                "Пользователь с id - %s, не найден",
                player_id,
            )
            raise WrongUserId(message="Ошибка пользователя")
        self.logger.info("id противника - %s")
        return enemy_id