from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

random_num_updated_cb_data = "random_num_updated_cb_data"

def buld_info_kd():
    tg_channel_bt = InlineKeyboardButton(
    text="Канал",
    url="https://t.me/+TRzHuBxuIxZlY2Qy"
    )
    pic = InlineKeyboardButton(
        text="Картинка",
        url="https://i.pinimg.com/736x/ac/15/8e/ac158efaaef7f12cbd837dac7ad0f0fe.jpg"
    )
    btn_random_site = InlineKeyboardButton(
        text="Start data",
        callback_data=random_num_updated_cb_data,
    )

    row = [tg_channel_bt, btn_random_site]
    row_1 = [pic]
    rows = [row, row_1]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup