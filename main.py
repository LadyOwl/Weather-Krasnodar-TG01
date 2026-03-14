import asyncio
import urllib.request
import json
import os
import time
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from config import BOT_TOKEN, WEATHER_API_KEY
from keyboards import get_start_keyboard, get_links_keyboard
from gtts import gTTS
from deep_translator import GoogleTranslator

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

os.makedirs("img", exist_ok=True)


# Команда /start с кнопками
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = get_start_keyboard()
    await message.answer("Выберите кнопку:", reply_markup=keyboard)


# Обработчик кнопки "Привет"
@dp.callback_query(F.data == "btn_hello")
async def btn_hello(callback: types.CallbackQuery):
    user_name = callback.from_user.first_name
    await callback.message.answer(f"Привет, {user_name}!")
    await callback.answer()


# Обработчик кнопки "Пока"
@dp.callback_query(F.data == "btn_bye")
async def btn_bye(callback: types.CallbackQuery):
    user_name = callback.from_user.first_name
    await callback.message.answer(f"До свидания, {user_name}!")
    await callback.answer()


# Команда /links с URL-кнопками
@dp.message(Command("links"))
async def cmd_links(message: types.Message):
    keyboard = get_links_keyboard()
    await message.answer("Выберите раздел:", reply_markup=keyboard)


# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    text = (
        "Доступные команды:\n"
        "/weather_now - запрос погоды в Краснодаре\n"
        "/translate - перевести текст на английский\n"
        "/links - полезные ссылки\n"
        "/start - приветствие\n"
        "/help - все доступные команды бота\n\n"
        "📝 Также я автоматически перевожу любой текст, который ты мне напишешь!"
    )
    await message.answer(text)


# Команда /weather_now
@dp.message(Command("weather_now"))
async def send_weather(message: types.Message):
    city = "Krasnodar"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        weather_text = f"🌤 Погода в Краснодаре:\nТемпература: {temp}°C\nУсловия: {description}"
        await message.answer(weather_text)

        voice_text = f"Погода в Краснодаре. Температура: {temp} градусов Цельсия. Условия: {description}."

        try:
            tts = gTTS(text=voice_text, lang='ru')
            filename = f"voice_{int(time.time())}.mp3"
            tts.save(filename)

            voice = FSInputFile(filename)
            await message.answer_voice(voice)

            os.remove(filename)
            print("✅ Голосовое отправлено и файл удалён")

        except Exception as voice_error:
            print(f"❌ Ошибка голоса: {voice_error}")
            await message.answer(f"🗣 Текст: {voice_text}")

    except Exception as e:
        print(f"❌ Ошибка погоды: {e}")
        await message.answer("Ошибка получения данных о погоде.")


# Команда /translate
@dp.message(Command("translate"))
async def cmd_translate(message: types.Message):
    await message.answer(
        "📝 **Как использовать перевод:**\n\n"
        "Просто отправь мне любой текст на русском языке, "
        "и я автоматически переведу его на английский!\n\n"
        "Пример:\n"
        "Ты: Привет, как дела?\n"
        "Я: 🇬🇧 Перевод: Hello, how are you?"
    )


# 🌐 Обработчик текста - перевод на английский
@dp.message(F.text)
async def translate_text(message: types.Message):
    if message.text.startswith('/'):
        return

    try:
        original_text = message.text
        translator = GoogleTranslator(source='auto', target='en')
        translated_text = translator.translate(original_text)

        await message.answer(f"🇬🇧 Перевод:\n\n{translated_text}")
        print(f"📝 Переведено: {original_text} → {translated_text}")

    except Exception as e:
        print(f"❌ Ошибка перевода: {e}")
        await message.answer("Не удалось перевести текст. Попробуйте позже.")


# Обработчик фото
@dp.message(F.photo)
async def save_photo(message: types.Message):
    try:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        file_path = file.file_path
        filename = f"img/photo_{int(time.time())}.jpg"

        await bot.download_file(file_path, filename)
        await message.answer("✅ Фото сохранено в папку img/")

    except Exception as e:
        print(f"Ошибка сохранения фото: {e}")
        await message.answer("Не удалось сохранить фото.")


# Запуск бота
async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())