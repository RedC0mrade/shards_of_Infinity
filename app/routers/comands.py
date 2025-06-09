import asyncio
import csv
import io
import logging
import aiohttp
from re import Match

from aiogram.utils.chat_action import ChatActionSender
from aiogram.client.default import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction, ParseMode
from magic_filter import RegexpMode


router = Router(name=__name__)


@router.message(CommandStart())  # CommandStart() Команда /start
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


@router.message(
    Command("help", prefix="!?+")
)  # Команда help может начинаться с "!" или "?" или "+"
async def handle_help(message: types.Message):
    text = (
        "<b>I'm an echo bot.</b>\n" "<i><b>Send me any!</b></i>"
    )  # Жирный текст и италик

    await message.answer(text=text)  # отправка ответа на текст, команду


@router.message(Command("pic"))  # Команда /pic
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


@router.message(
    Command("home_pic")  # Команда /home_pic вводится вручную, если нужна регистрация
)  # в панеле команд делается через botFather /setcommand
async def handel_command_home_pic(message: types.Message):
    file_path = "C:/Users/PC/Pictures/Screenshots/Снимок_экрана_2024-09-10_194528.png"
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
    await message.bot.send_photo(  # просто сообщение
        chat_id=message.chat.id,
        photo=types.FSInputFile(  # Загрузка фото с локального диска
            path=file_path,
        ),
        caption="cat photo",
    )


@router.message(Command("test", prefix="!"))  # Команда !test
async def send_text_file(message: types.Message):
    file = io.StringIO()  # Создание текстового файла
    file.write("Hellow world\n")  # Запись в текстовый файл
    file.write("World, hellow\n")
    await message.bot.send_document(
        chat_id=message.chat.id,
        document=types.BufferedInputFile(  # Берем фаил из буфера
            file=file.getvalue().encode("utf-8"),  # file изменяется в байт
            filename="text.txt",  # Название файла
        ),
    )


@router.message(Command("buffer"))
async def handel_command_home_pic(message: types.Message):
    """Если картинка по ссылке слишком большая и телеграмм не может её отправить
    и мы не хотим ее сохранять на жестком, но передаем её как документ"""
    url = (
        "https://lh4.googleusercontent.com/proxy/Vk7aF3D4OkLUpIb9GzrdTGAPkhQG"
        "ks7zbqdACzcYwHrW7CZmCu6a_298V6F1d0vNJDpJ3gAl9qXDJPy7U9xh0o8m5BdCyKZXF"
        "5YTg3iIz8a9SoqaG9GkESj_vi1dBXRp9PVWVbTQrIaK"
    )
    # await message.bot.send_chat_action(   # Чат экшен работает всего 5 секунд
    #     chat_id=message.chat.id,
    #     action=ChatAction.UPLOAD_DOCUMENT,
    # )

    async with ChatActionSender(  # ChatActionSender чат экшен работает все время пока отправляется фаил
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    ):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                result = await response.read()

        file = io.BytesIO()
        file.write(result)
        await message.bot.send_document(
            chat_id=message.chat.id,
            document=types.BufferedInputFile(
                file=file.getvalue(),  #  можно передать сразу result, getvalue()
                filename="big_pic.jpeg",
            ),
        )


@router.message(Command("file"))
async def handel_command_file(message: types.Message):
    file_path = "C:/Users/PC/Downloads/zapret-discord-youtube-1.7.2b.rar"
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    message_send = await message.reply_document(
        document=types.FSInputFile(path=file_path, filename="antizapret"),
        caption="Antizapret",
    )
    print(message_send.document.file_id)  # id для сохранения в базе и отправки повторно

@router.message(Command("csv"))
async def send_csv_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    file = io.StringIO()  # Фаил формируется в буфере
    csv_writer = csv.writer(file)
    csv_writer.writerows(
        [
            ["Name", "Age", "City"],
            ["John Smith", "28", "New York"],
            ["Jane Doe", "32", "Los Angeles"],
            ["Mike Johnson", "40", "Chicago"],
        ]
    )
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),  # необходимо перевести в байты
            filename="people.csv",  # Название файла
        ),
    )