from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.game import Game, GameStatus
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

    async def accept_game(
        self,
        game_data: InvateGameSchema
    ) -> Game:
        stmt = select(Game).where(Game.invite_token == game_data.invite_token)
        result: Result = self.session.execute(stmt)
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
