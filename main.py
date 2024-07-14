# файл main.py
import os
import asyncio
import logging
from telebot.async_telebot import AsyncTeleBot
import g4f
from g4f.client import AsyncClient
from g4f.Provider import You

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка бота
bot = AsyncTeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM Claude Sonet.')

# Асинхронная функция для обработки сообщений
@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    user_message = message.text
    client = AsyncClient(provider=You)
    response = await client.create(model='claude-3-sonnet', messages=[{"role": "user", "content": user_message}])
    await bot.send_message(message.chat.id, response['choices'][0]['message']['content'])

# Запуск бота
async def main():
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(main())
