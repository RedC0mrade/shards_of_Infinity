from fastapi import APIRouter, Depends

from app.backend.crud.users_crud import UserServices
from app.backend.factories.user_factory import get_user_service
from app.backend.schemas.users import UserCreateSchema, UserSchema


router = APIRouter(tags=["User"])


@router.post(
    "/create_user",
    response_model=UserSchema,
    status_code=201,
)
async def get_deck_of_cards(
    user_data: UserCreateSchema,
    user_service: UserServices = Depends(get_user_service),
):
    return await user_service.get_or_create_user(user_data=user_data)
