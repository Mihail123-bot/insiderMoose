import streamlit as st
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import threading

BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"
PAYMENT_ADDRESS = "EdFcVXCxo2c5VBi1FY4UAhuW9VhyM2S9uu3BRY9Whcj4"

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.app = None
        self.bot_thread = None
        self.is_running = False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command and send subscription plans."""
        keyboard = [[InlineKeyboardButton("Start Payment", callback_data="start_payment")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Do not miss out on this crazy community and join now!\nJust follow the instructions to complete the payment.",
            reply_markup=reply_markup
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button clicks."""
        query = update.callback_query
        await query.answer()

        if query.data == "start_payment":
            await query.message.reply_text(
                "Please select a plan:\n\n"
                "⚡️ *Basic: 0.1 SOL/month* ⚡️\n"
                "High quality signals ✅\n"
                "Late signals ✅\n"
                "Private tools ❌\n"
                "Private bots ❌\n"
                "Early signals ❌\n\n"
                "⚡️ *Standard: 0.25 SOL/month* ⚡️\n"
                "High quality signals ✅\n"
                "Late signals ✅\n"
                "Private tools ✅\n"
                "Private bots ❌\n"
                "Early signals ❌\n\n"
                "⚡️ *Pro: 1 SOL/month* ⚡️\n"
                "High quality signals ✅\n"
                "Late signals ✅\n"
                "Private tools ✅\n"
                "Private bots ✅\n"
                "Early signals ✅\n"
                "BONUS: Chatroom with whales and insiders ✅",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Basic Plan", callback_data="basic_plan")],
                    [InlineKeyboardButton("Standard Plan", callback_data="standard_plan")],
                    [InlineKeyboardButton("Pro Plan", callback_data="pro_plan")]
                ])
            )
        elif query.data in ["basic_plan", "standard_plan", "pro_plan"]:
            plan = query.data.replace("_plan", "").capitalize()
            await query.message.reply_text(
                f"You selected the {plan} Plan. Please send your wallet address from which the payment will go out."
            )
            context.user_data["selected_plan"] = plan

        elif query.data == "confirm_payment":
            selected_plan = context.user_data.get("selected_plan", "Unknown Plan")
            await query.message.reply_text(
                f"Thank you! You selected the {selected_plan} Plan.\n\n"
                f"Send the payment to the following address:\n\n`{PAYMENT_ADDRESS}`\n\n"
                "After completing the payment, click a button below to proceed.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Check Status", callback_data="check_status")],
                    [InlineKeyboardButton("Cancel", callback_data="cancel_payment")]
                ])
            )
        elif query.data == "check_status":
            await query.message.reply_text(
                "Payment status: Pending... (You can integrate this with a real Solana API to check status.)"
            )
        elif query.data == "cancel_payment":
            await query.message.reply_text("Payment canceled. You can restart the process with /start.")

    def _run_bot(self):
        """Run the Telegram bot in polling mode."""
        try:
            self.app = ApplicationBuilder().token(self.token).build()

            # Add handlers
            self.app.add_handler(CommandHandler("start", self.start_command))
            self.app.add_handler(CallbackQueryHandler(self.handle_callback))
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

# Initialize bot in Streamlit session state
if "bot" not in st.session_state:
    st.session_state.bot = TelegramBot(BOT_TOKEN)

def main():
    st.title("Telegram Bot Control Panel")
    st.write("Your Telegram bot is running and ready to process commands!")

    # Automatically start bot
    st.session_state.bot.start()

if __name__ == "__main__":
    main()
