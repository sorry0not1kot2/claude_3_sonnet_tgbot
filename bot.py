import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from g4f.client import AsyncClient
from g4f.Provider import You

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для общения с LLM Claude Sonet.')

# Асинхронная функция для обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    async with AsyncClient(provider=You) as client:
        response = await client.create(model='claude-3-sonnet', messages=[{"role": "user", "content": user_message}])
        await update.message.reply_text(response['choices'][0]['message']['content'])

def main() -> None:
    # Вставьте сюда ваш токен
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: asyncio.run(handle_message(update, context))))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
