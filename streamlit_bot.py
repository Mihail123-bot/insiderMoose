import streamlit as st
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Do not miss out on this crazy community and join now!")

def run_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()

def main():
    st.title("Insider Moose Bot")
    
    if st.button("Start Bot"):
        run_bot()

if __name__ == "__main__":
    main()

