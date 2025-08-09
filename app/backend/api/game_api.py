from fastapi import APIRouter, Depends

from app.backend.factories.game_factory import get_game_service
from app.backend.crud.games_crud import GameServices
from app.backend.schemas.games import CreateGameSchema, GameSchems, InvateGameSchema


router = APIRouter(tags=["Game"])


@router.post("/create_game", response_model=GameSchems)
async def create_game(
    game_data: CreateGameSchema,
    game_service: GameServices = Depends(get_game_service),
):
    return await game_service.create_game(game_data=game_data)


@router.post("/invite_game", response_model=GameSchems)
async def create_game(
    game_data: InvateGameSchema,
    game_service: GameServices = Depends(get_game_service),
):
    return await game_service.accept_game(game_data=game_data)