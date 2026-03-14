from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Кнопки для команды /start
def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Привет", callback_data="btn_hello")],
        [InlineKeyboardButton(text="Пока", callback_data="btn_bye")]
    ])
    return keyboard


# Кнопки для команды /links
def get_links_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📰 Новости", url="https://russian.rt.com/")],
        [InlineKeyboardButton(text="🎵 Музыка", url="https://europaplus.ru/")],
        [InlineKeyboardButton(text="🎬 Видео", url="https://vkvideo.ru/")]
    ])
    return keyboard

# Динамическая клавиатура - первый экран
def get_dynamic_keyboard_start():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Показать больше", callback_data="btn_show_more")]
    ])
    return keyboard


# Динамическая клавиатура - второй экран
def get_dynamic_keyboard_options():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ Узнать о боте", callback_data="btn_option_1")],
        [InlineKeyboardButton(text="👨‍💻 Контакты разработчика", callback_data="btn_option_2")]
    ])
    return keyboard