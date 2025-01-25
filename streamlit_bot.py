import streamlit as st
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

BOT_TOKEN = "7653877973:AAHfj_ks6hAvYzS4vXBk71WUV-qBSXr5vTo"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! I'm your Streamlit-powered bot.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    await update.message.reply_text(f"You said: {text}")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    await app.initialize()
    await app.start()
    st.write("Bot is running...")
    
    try:
        await app.updater.start_polling(drop_pending_updates=True)
        await asyncio.Event().wait()
    except Exception as e:
        st.error(f"Bot error: {e}")
    finally:
        await app.stop()

def main():
    st.title("Telegram Bot Control Panel")
    
    if st.button("Start Bot"):
        try:
            asyncio.run(run_bot())
        except Exception as e:
            st.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    main()
