import asyncio
import urllib.request
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN, WEATHER_API_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я покажу какая погода сейчас в Краснодаре😍")


# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    text = "Доступные команды:\n/weather_now - запрос погоды\n/start - приветствие\n/help - все доступные команды бота"
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

    except Exception as e:
        await message.answer("Ошибка получения данных о погоде.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())