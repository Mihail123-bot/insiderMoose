import os
import streamlit as st
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Retrieve bot token from secrets
TELEGRAM_BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! I'm your Streamlit-powered bot.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    await update.message.reply_text(f"You said: {text}")

async def run_bot():
    # Initialize Telegram Bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run bot
    await app.initialize()
    await app.start()
    st.write("Bot is running...")
    
    # Keep bot running
    while True:
        await asyncio.sleep(1)

def main():
    st.title("Telegram Bot Control Panel")
    
    # Use asyncio to run the bot
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
