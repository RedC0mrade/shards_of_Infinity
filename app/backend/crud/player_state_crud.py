from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.schemas.play_state import CreatePlayStateSchema


class Player_stateServices:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_play_state(
        self,
        play_data: CreatePlayStateSchema,
    ):
        pass
