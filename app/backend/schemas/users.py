from pydantic import BaseModel, PositiveInt


class UserCreateSchema(BaseModel):
    chat_id: PositiveInt
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserSchema(UserCreateSchema):
    id: PositiveInt
    victories: PositiveInt
    defeats: PositiveInt

