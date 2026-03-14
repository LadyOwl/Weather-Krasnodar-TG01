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
        [InlineKeyboardButton(text="📰 Новости", url="ВСТАВЬ_ССЫЛКУ_НА_НОВОСТИ")],
        [InlineKeyboardButton(text="🎵 Музыка", url="ВСТАВЬ_ССЫЛКУ_НА_МУЗЫКУ")],
        [InlineKeyboardButton(text="🎬 Видео", url="ВСТАВЬ_ССЫЛКУ_НА_ВИДЕО")]
    ])
    return keyboard