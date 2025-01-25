import streamlit as st
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import re
import threading

BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"

class SubscriptionBot:
    def __init__(self, token):
        self.token = token
        self.app = None
        self.user_states = {}
        self.bot_thread = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("Start Payment", callback_data='start_payment')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Do not miss out on this crazy community and join now! "
            "Just follow the instructions to complete the payment.",
            reply_markup=reply_markup
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == 'start_payment':
            keyboard = [
                [InlineKeyboardButton("⚡️Basic: 0.1 sol/month⚡️", callback_data='basic_0.1')],
                [InlineKeyboardButton("⚡️Basic: 0.25 sol/month⚡️", callback_data='basic_0.25')],
                [InlineKeyboardButton("⚡️Pro: 1 sol/month⚡️", callback_data='pro_1')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text(
                "Select Your Subscription Plan:\n\n"
                "⚡️Basic: 0.1 sol/month⚡️\n"
                "✅ High quality signals\n"
                "✅ Late signals\n"
                "❌ Private tools\n"
                "❌ Private bots\n"
                "❌ Early signals\n\n"
                "⚡️Basic: 0.25 sol/month⚡️\n"
                "✅ High quality signals\n"
                "✅ Late signals\n"
                "✅ Private tools\n"
                "❌ Private bots\n"
                "❌ Early signals\n\n"
                "⚡️Pro: 1 sol/month⚡️\n"
                "✅ High quality signals\n"
                "✅ Late signals\n"
                "✅ Private tools\n"
                "✅ Private bots\n"
                "✅ Early signals\n"
                "✅ BONUS: Chatroom with whales",
                reply_markup=reply_markup
            )
        
        elif query.data in ['basic_0.1', 'basic_0.25', 'pro_1']:
            plan_name = {
                'basic_0.1': 'Basic 0.1 sol/month',
                'basic_0.25': 'Basic 0.25 sol/month', 
                'pro_1': 'Pro 1 sol/month'
            }[query.data]
            
            self.user_states[query.from_user.id] = {'plan': plan_name}
            
            await query.message.edit_text(
                f"You selected the {plan_name}. Please send your wallet address from which the payment will go out."
            )

    async def handle_wallet_address(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        wallet = update.message.text

        if user_id not in self.user_states:
            await update.message.reply_text("Please select a plan first using /start")
            return

        if not re.match(r'^[A-Za-z0-9]{32,44}$', wallet):
            await update.message.reply_text("Invalid wallet address. Please try again.")
            return

        plan = self.user_states[user_id]['plan']
        keyboard = [
            [
                InlineKeyboardButton("Check Status", callback_data='check_status'),
                InlineKeyboardButton("Cancel", callback_data='cancel_payment')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Thank you! You selected the {plan}. "
            "Send the payment of Sol to the following address: "
            "EdFcVXCxo2c5VBi1FY4UAhuW9VhyM2S9uu3BRY9Whcj4",
            reply_markup=reply_markup
        )

    def _run_bot(self):
        try:
            self.app = ApplicationBuilder().token(self.token).build()
            
            self.app.add_handler(CommandHandler('start', self.start_command))
            self.app.add_handler(CallbackQueryHandler(self.button_callback))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_wallet_address))
            
            self.app.run_polling(drop_pending_updates=True)
        except Exception as e:
            st.error(f"Bot error: {e}")

    def start_bot(self):
        if not self.bot_thread or not self.bot_thread.is_alive():
            self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
            self.bot_thread.start()

def main():
    st.title("Telegram Subscription Bot")
    
    if 'bot' not in st.session_state:
        st.session_state.bot = SubscriptionBot(BOT_TOKEN)
    
    st.session_state.bot.start_bot()
    st.write("Bot is running. Open Telegram and start interaction.")

if __name__ == "__main__":
    main()
