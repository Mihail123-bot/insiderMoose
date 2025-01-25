import streamlit as st
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading

BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.app = None
        self.thread = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome! I'm your Streamlit-powered bot.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type = update.message.chat.type
        text = update.message.text
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
        await update.message.reply_text(f"You said: {text}")

    def start_bot(self):
        self.app = ApplicationBuilder().token(self.token).build()
        
        self.app.add_handler(CommandHandler('start', self.start_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        self.thread = threading.Thread(target=self.app.run_polling, kwargs={'drop_pending_updates': True})
        self.thread.start()

def main():
    st.title("Telegram Bot Control Panel")
    
    bot = TelegramBot(BOT_TOKEN)
    
    if st.button("Start Bot"):
        bot.start_bot()
        st.success("Bot started!")

if __name__ == "__main__":
    main()
