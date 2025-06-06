import asyncio
import csv
import io
import logging
from re import Match

from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction, ParseMode
from magic_filter import RegexpMode

from config import settings

dp = Dispatcher()


@dp.message(
    F.text.lower().regexp(
        r"too",
        mode=RegexpMode.SEARCH,
    )
)
async def echo_message_too(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    try:
        await message.forward(chat_id=message.chat.id)  # Пересылка сообщение
        # await message.copy_to(chat_id=message.chat.id) # Отправка копии
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new")


@dp.message(
    F.text.lower().regexp(
        r"foo",
        mode=RegexpMode.SEARCH,
    )
)
async def echo_message_foo(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    text = "No FoO"
    await message.bot.send_message(  # Просто отправка сообщения без ответа или форварда
        chat_id=message.chat.id,
        text=text,
    )


@dp.message(
    F.text.regexp(
        r"Bar",
        mode=RegexpMode.SEARCH,
    )
)
async def echo_message_bar(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    try:
        await message.forward(chat_id=message.chat.id)  # Пересылка сообщение
        # await message.copy_to(chat_id=message.chat.id) # Отправка копии
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new")


@dp.message(F.text)
async def echo_message(message: types.Message):
    await message.copy_to(chat_id=message.chat.id)


# @dp.message(Command("test", prefix="!"))  # Не работает
# async def send_text_file(message: types.Message):
#     file = io.StringIO()  # Создание текстового файла
#     file.write("Hellow world\n")  # Запись в текстовый файл
#     file.write("World, hellow\n")
#     await message.bot.send_document(
#         chat_id=message.chat.id,
#         document=types.BufferedInputFile(  # Берем фаил из буфера
#             file=file.getvalue().encode("utf-8"),  # file изменяется в байт
#             filename="text.txt",  # Название файла
#         ),
#     )


# @dp.message(Command("csv"))
# async def send_csv_file(message: types.Message):
#     await message.bot.send_chat_action(
#         chat_id=message.chat.id,
#         action=ChatAction.TYPING,
#     )
#     file = io.StringIO()
#     csv_writer = csv.writer(file)
#     csv_writer.writerows(
#         [
#             ["Name", "Age", "City"],
#             ["John Smith", "28", "New York"],
#             ["Jane Doe", "32", "Los Angeles"],
#             ["Mike Johnson", "40", "Chicago"],
#         ]
#     )
#     await message.reply_document(
#         document=types.BufferedInputFile(
#             file=file.getvalue().encode("utf-8"),
#             filename="people.csv",
#         ),
#     )


@dp.message(CommandStart())  # CommandStart() Команда /start
async def handle_start(message: types.Message):
    """Команда /start передает картинку"""
    url = (
        "https://cf.geekdo-images.com/GfQBoqOl21zQx-Vy-dSHZw__imagepagezoom/"
        "img/5cxdPGDSaEhGGm1lLkFGKt3-2iE=/fit-in/1200x900/filters:no_upscale():"
        "strip_icc()/pic4064509.png"
    )
    await message.answer(
        text=(
            f'<a href="{url}">&#8205;</a>'  # скрытая ссылка через zero-width space
            f"Hello, <b>{message.from_user.full_name}</b>!"
        ),
    )


@dp.message(
    Command("help", prefix="!?+")
)  # Команда help может начинаться с "!" или "?" или "+"
async def handle_help(message: types.Message):
    text = (
        "<b>I'm an echo bot.</b>\n" "<i><b>Send me any!</b></i>"
    )  # Жирный текст и италик

    await message.answer(text=text)  # отправка ответа на текст, команду


@dp.message(Command("pic"))  # Команда /pic
async def handel_command_pic(message: types.Message):
    url = (
        "https://img.freepik.com/free-vector/sweet-eyed-kitten-"
        "cartoon-character_1308-135596.jpg?semt=ais_hybrid&w=740"
    )
    await message.bot.send_chat_action(  # используется, чтобы показать пользователю, что бот "печатает" или выполняет действие (например, загружает фото, записывает голосовое или ищет данные).
        chat_id=message.chat.id,  # для отправки указывается id чата через мессадж
        action=ChatAction.UPLOAD_PHOTO,  # Показываем, что загружается фото
    )
    await message.reply_photo(
        photo=url,  # Ссылка на фото
        caption="cat photo",  # Описание фото
    )


@dp.message(
    Command("home_pic")  # Команда /home_pic вводится вручную, если нужна регистрация
)  # в панеле команд делается через botFather /setcommand
async def handel_command_home_pic(message: types.Message):
    file_path = "C:/Users/e2e4e/Pictures/IMG_20240802_183555[1].jpg"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    await message.reply_photo(  # reply это ответное сообщение
        photo=types.FSInputFile(  # Загрузка фото с локального диска
            path=file_path,
        ),
        caption="cat photo",
    )


@dp.message(Command("file"))
async def handel_command_file(message: types.Message):
    file_path = "C:/Users/e2e4e/Downloads/zapret-discord-youtube-1.7.2b.rar"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    message_send = await message.reply_document(
        document=types.FSInputFile(path=file_path, filename="antizapret"),
        caption="Antizapret",
    )
    print(message_send.document.file_id)  # id для сохранения в базе и отправки повторно


@dp.message(
    F.photo,  # попадают только отправленные фото
    ~F.caption,  # Без подписи
)
async def handle_message_no_caption(message: types.Message):
    caption = "i can't see photo"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply_photo(
        photo=message.photo[-1].file_id,  # Основное фото всегда последнее
        caption=caption,  # Устанавливаем собственное описание
    )


@dp.message(
    F.photo,  # Принимает фото
    F.caption.contains(
        "please"
    ),  # Где в описании фото есть слово "please" строгий регистр
)
async def handle_message_with_caption_please(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply(f"{str(message.caption)} please(0)")


@dp.message(
    F.photo,
    F.caption,  # Есть подпись
    # ~F.caption, # ~ означает, что описания нет
)
async def handle_message_with_caption(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,  # id чата
        action=ChatAction.TYPING,  # Бот передает что набирает текст
    )
    await message.reply(f"{str(message.caption)} contains some text!")


@dp.message(F.document | F.video)  # Принимает документы ИЛИ видео
async def handle_message_any_media(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    if message.document:
        await message.reply_document(
            document=message.document.file_id,
            caption=f"document {message.document.file_id}",
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id,
            caption=f"video {message.video.file_id}",
        )
    else:
        await message.reply("WTf is this?")


@dp.message(
    F.from_user.id.in_({1756123777}),
    F.text.lower() == "secret",
)  # from_user.id.in_({1756123777}) - передается список пользователей,
# для которых доступна команда secret не чувствительна к регистру
async def secret_admin_message(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply("hellow, admin")


@dp.message(
    F.text.regexp(
        r"\+7\(\d{3}\)(-\d{3})(-\d{2}){2}",
        mode=RegexpMode.SEARCH,
    ).as_("numder")
)
async def tel_message(message: types.Message, numder: Match[str]):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply(f"hellow, admin, {numder.group()}")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
