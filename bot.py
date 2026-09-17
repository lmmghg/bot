import asyncio
import logging
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен BOT_TOKEN не найден!")

logging.basicConfig(level=logging.INFO)

# --- Flask ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    logging.info(f"Запуск веб-сервера на порту {port}...")
    # use_reloader=False обязательно, иначе Flask попытается запуститься дважды
    app.run(host="0.0.0.0", port=port, use_reloader=False)

# --- Бот ---
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

async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    logging.info("Бот запущен и начинает polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Flask — в фоновом потоке (daemon=True, чтобы умер вместе с процессом)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Бот — в главном потоке
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")