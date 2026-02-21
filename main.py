import asyncio
import urllib.request
import json
import os
import time
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile  # ✅ Добавлено
from config import BOT_TOKEN, WEATHER_API_KEY
from gtts import gTTS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        # 📝 Текстовый ответ
        weather_text = f"🌤 Погода в Краснодаре:\nТемпература: {temp}°C\nУсловия: {description}"
        await message.answer(weather_text)

        # 🎤 Голосовое сообщение
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


async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())