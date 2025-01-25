from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TELEGRAM_TOKEN = "7653877973:AAEGkpqsEBF1SN60B5pC1wXj0HMa309fhJA"  # Your bot token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This is a test response.")

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    await application.initialize()
    await application.start()
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
