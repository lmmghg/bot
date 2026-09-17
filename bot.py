import asyncio
import logging
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем переменные окружения (для локального теста)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен BOT_TOKEN не найден! Добавьте его в переменные окружения.")

logging.basicConfig(level=logging.INFO)

# --- 1. Инициализация Flask ---
app = Flask(__name__)

# Маршрут, который Render будет использовать для проверки, что бот жив
@app.route("/")
def home():
    return "Bot is running successfully!"


# --- 2. Логика бота (ваш код) ---
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Напиши мне что-нибудь, и я повторю.")

@dp.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)

@dp.message()
async def fallback(message: Message):
    await message.answer("Я понимаю только текст 🙃")


# --- 3. Запуск бота в отдельном потоке ---
async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    logging.info("Бот запущен и начинает polling...")
    await dp.start_polling(bot)

def run_bot_thread():
    # Создаем новый event loop для этого потока
    asyncio.run(start_bot())

if __name__ == "__main__":
    # Запускаем бота в фоновом потоке (daemon=True), чтобы он не блокировал Flask
    bot_thread = threading.Thread(target=run_bot_thread, daemon=True)
    bot_thread.start()

    # Получаем порт от Render (или используем 8080 локально) и запускаем Flask
    port = int(os.environ.get("PORT", 8080))
    logging.info(f"Запуск веб-сервера на порту {port}...")
    app.run(host="0.0.0.0", port=port)