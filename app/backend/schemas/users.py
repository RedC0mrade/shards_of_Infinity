from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    chat_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserSchema(UserCreateSchema):
    id: int
