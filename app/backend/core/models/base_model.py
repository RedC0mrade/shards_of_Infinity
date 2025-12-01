import enum
from sqlalchemy import MetaData, Enum
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from config import settings


def CustomEnum(enum_cls: type[enum.Enum], name: str | None = None):
    """
    Создает строковый Enum, который хранится в БД как VARCHAR + CHECK.
    Использует .value элемента Enum.
    """
    return Enum(
        *(member.value for member in enum_cls),
        name=name,
        native_enum=False,
        validate_strings=True,
    )


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
