# файл main.py
import os
import asyncio
import logging
import nest_asyncio
from telebot.async_telebot import AsyncTeleBot
import g4f
from g4f.Provider import You
from nodriver import ChromeDriver

# Применение nest_asyncio
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Настройка ChromeDriver с параметром no_sandbox
chrome_options = ChromeDriver.Options()
chrome_options.add_argument("--no-sandbox")

# Обработчик команды /start
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM Claude Sonet.')

# Асинхронная функция для обработки сообщений
async def handle_message(message):
    user_message = message.text
    response = await g4f.ChatCompletion.create(provider=You, model='claude-3-sonnet', messages=[{"role": "user", "content": user_message}], options=chrome_options)
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
