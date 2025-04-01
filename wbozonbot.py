import asyncio
import logging
import os
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

# === Переменные окружения ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Логи ===
logging.basicConfig(level=logging.INFO)

# === OpenAI клиент ===
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# === Обработка сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    logging.info(f"Сообщение от {update.effective_user.username}: {user_input}")

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты помощник продавца на Wildberries и Ozon. Отвечай только по этим маркетплейсам, чётко, кратко и по делу. Не отклоняйся от темы, даже если вопрос сформулирован неполно."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        reply = "Произошла ошибка при обращении к GPT."

    await update.message.reply_text(reply)

# === Запуск приложения ===
async def main():
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Бот запущен")
    await app.run_polling()

# === Запуск с поддержкой Windows и nest_asyncio ===
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
