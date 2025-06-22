from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

random_num_updated_cb_data = "random_num_updated_cb_data"
random_num_start_desctop = "random_num_start_desctop"
def buld_info_kd():
    tg_channel_bt = InlineKeyboardButton(
    text="Канал",
    url="https://t.me/+TRzHuBxuIxZlY2Qy"
    )
    pic = InlineKeyboardButton(
        text="Картинка",
        url="https://i.pinimg.com/736x/ac/15/8e/ac158efaaef7f12cbd837dac7ad0f0fe.jpg"
    )
    btn_random_start = InlineKeyboardButton(
        text="Start data",
        callback_data=random_num_updated_cb_data,
    )
    btn_random_start_desktop = InlineKeyboardButton(
        text="Desctop start",
        callback_data=random_num_start_desctop,
    )

    row = [tg_channel_bt, btn_random_start]
    row_1 = [pic, btn_random_start_desktop]
    rows = [row, row_1]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup