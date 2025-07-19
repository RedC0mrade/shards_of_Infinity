from fastapi import APIRouter, Depends

from app.backend.factories.card_factories import get_card_service
from app.backend.schemas.card import CardSchema, CreateCardSchema
from app.backend.crud.card_crud import CardServices



router = APIRouter(tags=["Card"])

@router.get(
    "/get_card_deck",
    response_model=list[CreateCardSchema]
)
async def get_deck_of_cards(
    card_service: CardServices = Depends(get_card_service),
):
    return await card_service.