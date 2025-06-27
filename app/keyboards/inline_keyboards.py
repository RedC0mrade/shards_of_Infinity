from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineButtonText:
    random_num_updated_cb_data = "random_num_updated_cb_data"
    random_num_start_desctop = "random_num_start_desctop"
    random_num_start = "random_num_start"
    random_int = "random_int"
    random_int_1 = "random_int_1"
    random_int_2 = "random_int_2"
    random_int_3 = "random_int_3"


def buld_info_kd() -> InlineKeyboardMarkup:
    tg_channel_bt = InlineKeyboardButton(
        text="Канал", url="https://t.me/+TRzHuBxuIxZlY2Qy"
    )
    pic = InlineKeyboardButton(
        text="Картинка",
        url="https://i.pinimg.com/736x/ac/15/8e/ac158efaaef7f12cbd837dac7ad0f0fe.jpg",
    )
    btn_random_start = InlineKeyboardButton(
        text="Start data",
        callback_data=InlineButtonText.random_num_updated_cb_data,
    )
    btn_random_start_desktop = InlineKeyboardButton(
        text="Desctop start",
        callback_data=InlineButtonText.random_num_start_desctop,
    )
    btn_random_start_button = InlineKeyboardButton(
        text="random_num_start",
        callback_data=InlineButtonText.random_num_start,
    )
    btn_random_num = InlineKeyboardButton(
        text="random number",
        callback_data=InlineButtonText.random_int,
    )
    btn_random_num_1 = InlineKeyboardButton(
        text="random number_1",
        callback_data=InlineButtonText.random_int_1,
    )
    btn_random_num_2 = InlineKeyboardButton(
        text="random number_2",
        callback_data=InlineButtonText.random_int_2,
    )
    row = [tg_channel_bt, btn_random_start, btn_random_num]
    row_1 = [pic, btn_random_start_desktop, btn_random_num_1]
    row_2 = [btn_random_num_2, btn_random_start_button]
    rows = [row, row_1, row_2]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
