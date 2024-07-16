import os
import asyncio
import logging
import nest_asyncio
from telebot.async_telebot import AsyncTeleBot
import g4f
from g4f.Provider import You
import undetected_chromedriver as uc
import base64

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
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        
        driver = uc.Chrome(options=chrome_options, no_sandbox=True)
        auth_header = get_auth()
        response = await g4f.ChatCompletion.create(provider=You, model='claude-3-sonnet', messages=[{"role": "user", "content": user_message}], driver=driver, headers={"Authorization": auth_header})
        await bot.send_message(message.chat.id, response['choices'][0]['message']['content'])
        driver.quit()
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        await bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего сообщения.")

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
