from random import choice
from fastapi import HTTPException, status
from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.user import TelegramUser
from app.backend.schemas.games import CreateGameSchema, InvateGameSchema
from app.utils.exceptions.exceptions import HaveActiveGame
from app.utils.logger import get_logger


class GameServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)

    async def create_game(
        self,
        game_data: CreateGameSchema,
    ) -> Game:
        self.logger.info(
            "Создание игры для игрока %s с токеном %s",
            game_data.player1_id,
            game_data.invite_token,
        )
        game = Game(**game_data.model_dump())

        self.session.add(game)
        await self.session.commit()
        self.logger.debug("Игра создана: %s", game)
        await self.session.refresh(game)

        return game

    async def accept_game(self, game_data: InvateGameSchema) -> Game:
        self.logger.info(
            "Принятие игры для игрока %s",
            game_data.player2_id,
        )
        stmt = select(Game).where(Game.invite_token == game_data.invite_token)
        result: Result = await self.session.execute(stmt)
        game: Game = result.scalar_one_or_none()
        self.logger.info("Игра %s существует", game)
        if not game:
            self.logger.critical("Game not found")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid invitation link.",
            )
        game.player2_id = game_data.player2_id
        game.status = GameStatus.IN_PROGRESS

        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        self.logger.info(
            "Game %s accept with staus %s",
            game.id,
            game.status,
        )
        return game

    async def has_active_game(self, player_id: int) -> Game | bool:
        self.logger.info("player id %s", player_id)
        stmt = (
            select(Game)
            .where(
                or_(
                    Game.player1_id == player_id,
                    Game.player2_id == player_id,
                ),
                Game.status == GameStatus.IN_PROGRESS,
            )
            .limit(1)
        )
        result: Result = await self.session.execute(stmt)
        game = result.scalar_one_or_none()
        if game:
            self.logger.debug(
                "the game %s has already started status %s",
                game.id,
                game.status,
            )
            # return True
            raise HaveActiveGame(message="❌ У вас уже есть активная игра.")
        self.logger.warning("game not found")
        return False

    async def join_game_by_code(
        self,
        token: str,
        player2_id: int,
    ) -> Game:
        self.logger.info(
            "Попытка присоединиться к игре с кодом %s для игрока %s",
            token,
            player2_id,
        )
        stmt = select(Game).where(
            Game.invite_token == token,
            Game.status == GameStatus.WAITING,
        )
        result: Result = await self.session.execute(stmt)
        game: Game = result.scalar_one_or_none()
        if not game:
            self.logger.warning(
                "Игра с кодом %s не найдена или не в статусе WAITING", token
            )
            return None

        game.player2_id = player2_id
        game.active_player_id = choice([player2_id, game.player1_id])
        game.non_active_player_id = (
            game.player1_id
            if game.active_player_id == player2_id
            else player2_id
        )
        game.status = GameStatus.IN_PROGRESS
        await self.session.commit()
        await self.session.refresh(game)
        self.logger.info(
            "Игрок %s присоединился к игре %s. Активный игрок: %s",
            player2_id,
            game.id,
            game.active_player_id,
        )
        return game

    async def defeat(
        self,
        player_id: int,
    ):
        self.logger.info("Игрок %s терпит поражение", player_id)

        stmt = (
            select(Game)
            .where(
                or_(
                    Game.player1_id == player_id,
                    Game.player2_id == player_id,
                ),
                Game.status == GameStatus.IN_PROGRESS,
            )
            .limit(1)
        )
        result: Result = await self.session.execute(stmt)
        game: Game = result.scalar_one_or_none()
        if not game:
            self.logger.error(
                "Активная игра для игрока %s не найдена",
                player_id,
            )
            raise ValueError(f"Active game not found for player {player_id}")
        game.status = GameStatus.FINISHED
        player2_id = (
            game.player1_id if game.player1_id != player_id else game.player2_id
        )
        stmt = select(TelegramUser).where(TelegramUser.id == player_id)
        result: Result = await self.session.execute(stmt)
        loser: TelegramUser = result.scalar_one_or_none()
        if not loser:
            self.logger.error(
                "Игрок %s (проигравший) не найден в базе",
                player_id,
            )
            raise ValueError(f"User {player_id} not found")
        loser.defeats += 1

        stmt = select(TelegramUser).where(TelegramUser.id == player2_id)
        result: Result = await self.session.execute(stmt)
        winner: TelegramUser = result.scalar_one_or_none()
        if not winner:
            self.logger.error(
                "Игрок %s (победитель) не найден в базе",
                player2_id,
            )
            raise ValueError(f"User {player2_id} not found")
        winner.victories += 1

        self.session.add_all([game, loser, winner])
        await self.session.commit()
        self.logger.info(
            "Игра %s завершена. Победитель: %s, проигравший: %s",
            game.id,
            winner.id,
            loser.id,
        )

    async def delete_game(self, game_id: int):
        self.logger.warning("Удаление игры %s", game_id)
        stmt = delete(Game).where(Game.id == game_id)
        await self.session.execute(stmt)
        await self.session.commit()
        self.logger.info("Игра с id %s успешно удалена", game_id)

    async def get_active_game(self, player_id: int) -> Game:
        self.logger.info("Получение id игры пользователем id - %s", player_id)
        stmt = select(Game).where(
            Game.status == GameStatus.IN_PROGRESS,
            or_(
                Game.player1_id == player_id,
                Game.player2_id == player_id,
            ),
        )
        result: Result = await self.session.execute(stmt)
        game = result.scalar_one_or_none()
        if not game:
            self.logger.warning(
                "Нет активной игры у пользователя c id %s",
                player_id,
            )
            return None
        return game