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
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Обработчик команды /start
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM Claude Sonet.')

# Асинхронная функция для обработки сообщений
async def handle_message(message):
    user_message = message.text
    client = AsyncClient(provider=You)
    response = await client.chat(model='claude-3-sonnet', messages=[{"role": "user", "content": user_message}])
    await bot.send_message(message.chat.id, response['choices'][0]['message']['content'])

# Добавление обработчиков
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(handle_message, content_types=['text'])

# Асинхронная функция main для запуска бота
async def main():
    logging.info("Бот запущен")
    await bot.polling(non_stop=True, timeout=60)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
