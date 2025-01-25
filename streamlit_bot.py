import os
import streamlit as st
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your actual bot token - DO NOT hardcode in production!
TELEGRAM_BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! I'm your Streamlit-powered bot.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Simple echo bot
    await update.message.reply_text(f"You said: {text}")

def main():
    # Streamlit UI
    st.title("Telegram Bot Control Panel")
    st.write("Bot is running...")

    # Initialize Telegram Bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run bot in background
    st.write("Starting bot polling...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
