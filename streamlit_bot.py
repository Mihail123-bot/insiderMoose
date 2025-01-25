import streamlit as st
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import threading

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your actual token
WALLET_ADDRESS = "EdFcVXCxo2c5VBi1FY4UAhuW9VhyM2S9uu3BRY9Whcj4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Start Payment", callback_data="show_plans")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Do not miss out on this crazy community and join now! Just follow the instructions to complete the payment.",
        reply_markup=reply_markup
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
BONUS: Chatroom with whales and insiders ✅
"""
        keyboard = [
            [InlineKeyboardButton("Basic (0.1 SOL)", callback_data="plan_basic_01")],
            [InlineKeyboardButton("Basic (0.25 SOL)", callback_data="plan_basic_025")],
            [InlineKeyboardButton("Pro (1 SOL)", callback_data="plan_pro")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(plans_text, reply_markup=reply_markup)

def run_telegram_bot():
    async def start_bot():
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(callback_handler))
        
        await application.initialize()
        await application.start()
        await application.run_polling(drop_pending_updates=True)  # Added drop_pending_updates

    asyncio.run(start_bot())

def main():
    st.title("Telegram Payment Bot")
    
    if 'bot_running' not in st.session_state:
        st.session_state.bot_running = False
        st.session_state.bot_thread = None

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Start Bot"):
            if not st.session_state.bot_running:
                st.session_state.bot_thread = threading.Thread(target=run_telegram_bot)
                st.session_state.bot_thread.start()
                st.session_state.bot_running = True
                st.success("Bot is now running! Send /start in Telegram")
                
    with col2:
        if st.button("🛑 Stop Bot"):
            if st.session_state.bot_running:
                st.session_state.bot_running = False
                st.experimental_rerun()

    # Status Display
    st.sidebar.header("Bot Status")
    if st.session_state.bot_running:
        st.sidebar.success("🟢 Bot is Active")
    else:
        st.sidebar.error("🔴 Bot is Inactive")

if __name__ == "__main__":
    main()
