import streamlit as st
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import threading

BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"
WALLET_ADDRESS = "EdFcVXCxo2c5VBi1FY4UAhuW9VhyM2S9uu3BRY9Whcj4"

class PaymentBot:
    def __init__(self, token):
        self.token = token
        self.app = None
        self.bot_thread = None
        self.is_running = False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[InlineKeyboardButton("Start Payment", callback_data="show_plans")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Do not miss out on this crazy community and join now! Just follow the instructions to complete the payment.",
            reply_markup=reply_markup
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        if query.data == "show_plans":
            plans_text = """
⚡️Basic: 0.1 sol/month⚡️
High quality signals ✅
Late signals ✅
Access to private tools ❌
Access to private bots ❌
Early signals ❌

⚡️Basic: 0.25 sol/month⚡️
High quality signals ✅
Late signals ✅
Access to private tools ✅
Access to private bots ❌
Early signals ❌

⚡️Pro: 1 sol/month⚡️
High quality signals ✅
Late signals ✅
Access to private tools ✅
Access to private bots ✅
Early signals ✅
BONUS: Chatroom with whales and insiders ✅"""
            
            keyboard = [
                [InlineKeyboardButton("Basic (0.1 SOL)", callback_data="plan_basic_01")],
                [InlineKeyboardButton("Basic (0.25 SOL)", callback_data="plan_basic_025")],
                [InlineKeyboardButton("Pro (1 SOL)", callback_data="plan_pro")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(plans_text, reply_markup=reply_markup)
        
        elif query.data.startswith("plan_"):
            await query.message.reply_text(f"Please send your wallet address from which the payment will go out.")
            context.user_data['awaiting_wallet'] = True
            context.user_data['selected_plan'] = query.data

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get('awaiting_wallet'):
            wallet = update.message.text
            keyboard = [
                [InlineKeyboardButton("Check Status", callback_data="check_status")],
                [InlineKeyboardButton("Cancel", callback_data="cancel")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"Thank you! Send the payment to: {WALLET_ADDRESS}",
                reply_markup=reply_markup
            )
            context.user_data['awaiting_wallet'] = False

    def _run_bot(self):
        try:
            self.app = ApplicationBuilder().token(self.token).build()
            self.app.add_handler(CommandHandler('start', self.start_command))
            self.app.add_handler(CallbackQueryHandler(self.handle_callback))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            self.app.run_polling(drop_pending_updates=True)
        except Exception as e:
            st.error(f"Bot error: {e}")

    def start(self):
        if not self.is_running:
            self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
            self.bot_thread.start()
            self.is_running = True
            st.success("Payment Bot is active and ready to process transactions!")

if 'bot' not in st.session_state:
    st.session_state.bot = PaymentBot(BOT_TOKEN)

def main():
    st.title("Telegram Payment Bot Dashboard")
    st.session_state.bot.start()
    
    st.sidebar.header("Bot Statistics")
    st.sidebar.metric("Active Users", "0")
    st.sidebar.metric("Pending Payments", "0")

if __name__ == "__main__":
    main()
