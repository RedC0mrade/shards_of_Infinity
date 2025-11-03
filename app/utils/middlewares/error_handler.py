from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from typing import Callable, Awaitable, Any

from app.utils.exceptions.exceptions import GameError
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ErrorHandlerMiddleware(BaseMiddleware):
    """Централизованная обработка ошибок GameError."""

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)

        except GameError as e:
            logger.warning("Игровая ошибка: %s", e.message)

            # Если это callback — покажем alert
            if isinstance(event, CallbackQuery):
                await event.answer(text=e.message, show_alert=True)
            # Если обычное сообщение
            elif isinstance(event, Message):
                await event.answer(text=e.message)
            return

        except Exception as e:
            logger.exception("Непредвиденная ошибка: %s", e)
            # В случае callback показываем пользователю нейтральное сообщение
            if isinstance(event, CallbackQuery):
                await event.answer(
                    text="Произошла ошибка. Попробуйте позже.",
                    show_alert=True,
                )
            elif isinstance(event, Message):
                await event.answer("Произошла ошибка. Попробуйте позже.")
            return
