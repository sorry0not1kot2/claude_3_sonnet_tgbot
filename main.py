import os
import asyncio
import logging
import nest_asyncio
from telebot.async_telebot import AsyncTeleBot
import g4f
from g4f.Provider import You
import base64
import requests

# Применение nest_asyncio
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Функция для получения токена аутентификации
def get_auth() -> str:
    auth_uuid = "507a52ad-7e69-496b-aee0-1c9863c7c819"
    auth_token = f"public-token-live-{auth_uuid}:public-token-live-{auth_uuid}"
    auth = base64.standard_b64encode(auth_token.encode()).decode()
    return f"Basic {auth}"

# Обработчик команды /start
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM Claude Sonet.')

# Асинхронная функция для обработки сообщений
async def handle_message(message):
    try:
        user_message = message.text
        auth_header = get_auth()
        headers = {"Authorization": auth_header}
        data = {
            "model": "claude-3-sonnet",
            "messages": [{"role": "user", "content": user_message}]
        }
        response = requests.post("https://api.you.com/v1/chat/completions", headers=headers, json=data)
