from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.models.game import Game, GameStatus
from app.backend.schemas.games import CreateGameSchema


class GameServices:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create_game(
        self,
        player1_id: int,
        invite_token: str,
    ) -> Game:
        game = Game(
            player1_id=player1_id,
            invite_token=invite_token,
            active_player_id=player1_id,
        )
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)

        return game

    async def accept_game(
        self,
        player2_id: int,
        invite_token: str,
    ) -> Game:
        stmt = select(Game).where(Game.invite_token == invite_token)
        result: Result = self.session.execute(stmt)
        game: Game = result.scalar_one_or_none()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid invitation link.",
            )
        game.player2_id = player2_id
        game.invite_token = invite_token
        game.status = GameStatus.IN_PROGRESS

        self.session.add(game)
        await self.session.commit()
