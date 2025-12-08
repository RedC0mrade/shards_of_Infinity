class GameError(Exception):
    """Базовое исключение для игровых ошибок, показываемых пользователю."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class WrongUserId(GameError):
    """Не правильно указан id."""

    pass


class GameTokenError(GameError):
    """Ошибка, ввeдeн не верный токен."""

    pass


class ActiveGameError(GameError):
    """Пробле с активной игрой."""

    pass


class MarketError(GameError):
    """Ошибка маркета."""

    pass


class NotEnoughCrystals(GameError):
    """Недостаточно кристаллов для покупки карты."""

    pass


class InvalidCardZone(GameError):
    """Карта выбрана неверно."""

    pass


class NotYourTurn(GameError):
    """Попытка действия не в свой ход."""

    pass


class DoNotHaveCardInZone(GameError):
    """В данной зоне нет карт."""

    pass


class Invulnerability(GameError):
    """Невозможно атаковать."""

    pass


class ChampionError(GameError):
    """Проблема с чемпионом."""

    pass

class CardInstanceError(GameError):
    """Проблема с состоянием карты."""

    pass


class MasteryError(GameError):
    """Мастерство уже разыграно"""

    pass

class ConcentrationError(GameError):
    """Невозможно получить могущество."""

    pass
