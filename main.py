import os
import asyncio
import logging
import base64
from telebot.async_telebot import AsyncTeleBot
import g4f

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
@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM Claude Sonnet.')

# Асинхронная функция для обработки сообщений
@bot.message_handler(content_types=['text'])
async def handle_message(message):
    try:
        user_message = message.text
        auth_header = get_auth()
        headers = {"Authorization": auth_header}
        data = {
            "model": "claude-3-sonnet",
            "messages": [{"role": "user", "content": user_message}]
        }
        
        # Логирование запроса
        logging.info(f"URL: https://api.you.com/v1/chat/completions")
        logging.info(f"Заголовки: {headers}")
        logging.info(f"Данные: {data}")
        
        response = await g4f.ChatCompletion.create(
            model="claude-3-sonnet",
            messages=[{"role": "user", "content": user_message}],
            headers=headers
        )
        
        # Логирование статуса и текста ответа
        logging.info(f"Статус ответа: {response.status}")
        response_text = response.text
        logging.info(f"Текст ответа: {response_text}")
        
        # Проверка на пустой ответ
        if response.status != 200 or not response_text:
            raise ValueError("Пустой или некорректный ответ от API")
        
        response_data = response.json()
        await bot.send_message(message.chat.id, response_data['choices'][0]['message']['content'])
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        await bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего сообщения.")

# Асинхронная функция main для запуска бота
async def main():
    logging.info("Бот запущен")
    await bot.polling(non_stop=True)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
