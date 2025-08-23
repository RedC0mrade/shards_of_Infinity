from random import choice
from fastapi import HTTPException, status
from sqlalchemy import Result, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.game import Game, GameStatus
from app.backend.core.models.user import TelegramUser
from app.backend.schemas.games import CreateGameSchema, InvateGameSchema


class GameServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create_game(
        self,
        game_data: CreateGameSchema,
    ) -> Game:

        game = Game(**game_data.model_dump())

        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)

        return game

    async def accept_game(self, game_data: InvateGameSchema) -> Game:
        stmt = select(Game).where(Game.invite_token == game_data.invite_token)
        result: Result = await self.session.execute(stmt)
        game: Game = result.scalar_one_or_none()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid invitation link.",
            )
        game.player2_id = game_data.player2_id
        game.status = GameStatus.IN_PROGRESS

        self.session.add(game)
        await self.session.commit()
        return game

    async def has_active_game(self, player_id: int) -> bool:
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

        return result.scalar_one_or_none() is not None

    async def join_game_by_code(
        self,
        token: str,
        player2_id: int,
    ) -> Game | None:
        stmt = select(Game).where(
            Game.invite_token == token,
            Game.status == GameStatus.WAITING,
        )
        result: Result = await self.session.execute(stmt)
        game: Game = result.scalar_one_or_none()
        if not game:
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
        return game

    async def defeat(
        self,
        player_id: int,
    ):
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
            raise ValueError(f"Active game not found for player {player_id}")
        game.status = GameStatus.FINISHED
        player2_id = (
            game.player1_id if game.player1_id != player_id else game.player2_id
        )
        stmt = select(TelegramUser).where(TelegramUser.id == player_id)
        result: Result = await self.session.execute(stmt)
        loser: TelegramUser = result.scalar_one_or_none()
        if not loser:
            raise ValueError(f"User {player_id} not found")
        loser.defeats += 1

        stmt = select(TelegramUser).where(TelegramUser.id == player2_id)
        result: Result = await self.session.execute(stmt)
        winner: TelegramUser = result.scalar_one_or_none()
        if not winner:
            raise ValueError(f"User {player2_id} not found")
        winner.victories += 1

        self.session.add_all([game, loser, winner])
        await self.session.commit()