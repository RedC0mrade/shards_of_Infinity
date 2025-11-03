class GameError(Exception):
    """Базовое исключение для игровых ошибок, показываемых пользователю."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotEnoughCrystals(GameError):
    """Недостаточно кристаллов для покупки карты."""
    pass


class InvalidCardZone(GameError):
    """Карта выбрана неверно."""
    pass


class NotYourTurn(GameError):
    """Попытка действия не в свой ход."""
    pass
