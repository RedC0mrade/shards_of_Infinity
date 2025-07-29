from typing import List
from fastapi import APIRouter, Depends

from app.backend.factories.card_factories import get_card_service
from app.backend.schemas.card import CardSchema, CreateCardSchema
from app.backend.crud.card_crud import CardServices


router = APIRouter(tags=["Card"])


@router.get("/get_card_deck", response_model=list[CardSchema])
async def get_deck_of_cards(
    card_service: CardServices = Depends(get_card_service),
):
    return await card_service.get_all_cards_in_the_deck()


@router.post(
    "/create_card",
    response_model=CardSchema,
    status_code=201,
)
async def get_deck_of_cards(
    card_data: CreateCardSchema,
    card_service: CardServices = Depends(get_card_service),
):
    return await card_service.create_card(card_data=card_data)


@router.post(
    "/create_cards",
    response_model=list[CardSchema],
    status_code=201,
)
async def get_deck_of_cards(
    cards_data: list[CreateCardSchema],
    card_service: CardServices = Depends(get_card_service),
):
    return await card_service.create_all_cards(cards_data=cards_data)