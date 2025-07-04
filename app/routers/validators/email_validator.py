from aiogram import types
from pydantic import validate_email


def valid_email(email: str) -> str:
    if "@" not in email or "." not in email:
        raise ValueError("Invalid email")
    return email.lower()


def valid_email_filter(message: types.Message) -> dict[str, str] | None:
    try:
        email = valid_email(message.text)
    except ValueError:
        return None
    return {"email": email}