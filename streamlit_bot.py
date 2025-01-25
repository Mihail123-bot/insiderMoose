import streamlit as st
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading

BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTos"

class PersistentTelegramBot:
    def __init__(self, token):
        self.token = token
        self.app = None
        self.bot_thread = None
        self.is_running = False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome! I'm your always-on Streamlit bot.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        await update.message.reply_text(f"You said: {text}")

    def _run_bot(self):
        try:
            self.app = ApplicationBuilder().token(self.token).build()
            self.app.add_handler(CommandHandler('start', self.start_command))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            self.app.run_polling(drop_pending_updates=True)
        except Exception as e:
            st.error(f"Bot error: {e}")

    def start(self):
        if not self.is_running:
            self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
            self.bot_thread.start()
            self.is_running = True
            st.success("Bot started and will remain active!")

# Initialize bot outside main to persist across reruns
if 'bot' not in st.session_state:
    st.session_state.bot = PersistentTelegramBot(BOT_TOKEN)

def main():
    st.title("Telegram Bot Control Panel")
    
    # Automatically start bot on page load
    st.session_state.bot.start()

if __name__ == "__main__":
    main()
