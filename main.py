import asyncio
import urllib.request
import json
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from config import BOT_TOKEN, WEATHER_API_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем папку для фото, если нет
os.makedirs("img", exist_ok=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я покажу какая погода сейчас в Краснодаре😍")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    text = "Доступные команды:\n/weather_now - запрос погоды\n/start - приветствие\n/help - все доступные команды бота"
    await message.answer(text)


@dp.message(Command("weather_now"))
async def send_weather(message: types.Message):
    city = "Krasnodar"
    # Исправлена ссылка (убраны лишние пробелы)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        weather_text = f"🌤 Погода в Краснодаре:\nТемпература: {temp}°C\nУсловия: {description}"
        await message.answer(weather_text)

    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Ошибка получения данных о погоде.")


# Обработчик фото
@dp.message(F.photo)
async def save_photo(message: types.Message):
    try:
        # Берем фото в максимальном качестве (последнее в списке)
        photo = message.photo[-1]

        # Скачиваем файл
        file = await bot.get_file(photo.file_id)
        file_path = file.file_path

        # Уникальное имя файла
        import time
        filename = f"img/photo_{int(time.time())}.jpg"

        await bot.download_file(file_path, filename)

        await message.answer("✅ Фото сохранено в папку img/")

    except Exception as e:
        print(f"Ошибка сохранения фото: {e}")
        await message.answer("Не удалось сохранить фото.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())