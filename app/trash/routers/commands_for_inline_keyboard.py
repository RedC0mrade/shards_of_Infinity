from aiogram import Bot, F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ChatAction

from app.keyboards.inline_keyboards import buld_info_kd
from app.keyboards.actions_keyboards import actions_kb_bulder

router = Router(name=__name__)


@router.message(Command("info", prefix="/!"))
async def handel_info_command(message: types.Message):
    async with ChatActionSender(  # ChatActionSender чат экшен работает все время пока отправляется фаил
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    ):
        await message.bot.send_message(
            chat_id=message.chat.id,
            text="Ссылки и прочие ресурсы",
            reply_markup=buld_info_kd(),
        )

@router.message(Command("action", prefix="!/"))
async def handle_action_command(message: types.Message):
    async with ChatActionSender(  # ChatActionSender чат экшен работает все время пока отправляется фаил
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    ):
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=" Ваши действия",
            reply_markup=actions_kb_bulder(),
        )