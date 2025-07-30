from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    telegramm_id: int
    first_name: str | None = None
    last_name: str | None = None