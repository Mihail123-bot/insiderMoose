import streamlit as st
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"

# Persistent Telegram Bot Class
class PersistentTelegramBot:
    def __init__(self, token):
        self.token = token
        self.app = None
        self.bot_thread = None
        self.is_running = False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        await update.message.reply_text("Welcome! I'm your always-on Streamlit bot.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages."""
        text = update.message.text
        await update.message.reply_text(f"You said: {text}")

    def _run_bot(self):
        """Run the Telegram bot in polling mode."""
        try:
            self.app = ApplicationBuilder().token(self.token).build()
            # Add Command and Message Handlers
            self.app.add_handler(CommandHandler('start', self.start_command))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            self.app.run_polling(drop_pending_updates=True)
        except Exception as e:
            st.error(f"Bot error: {e}")

    def start(self):
        """Start the bot in a separate thread."""
        if not self.is_running:
            self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
            self.bot_thread.start()
            self.is_running = True
            st.success("Bot started and will remain active!")

# Initialize the bot and persist it across Streamlit sessions
if 'bot' not in st.session_state:
    st.session_state.bot = PersistentTelegramBot(BOT_TOKEN)

# Main Streamlit App
def main():
    st.title("Telegram Bot Control Panel")
    st.write("This bot will remain active as long as the app is running.")
    
    # Auto-start the bot when the app loads
    st.session_state.bot.start()

if __name__ == "__main__":
    main()
