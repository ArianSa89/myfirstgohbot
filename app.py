import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler

# --- TELEGRAM BOT LOGIC ---
async def start(update, context):
    """Handler for the /start command"""
    await update.message.reply_text("Hello! I am your simple bot.")

async def hello(update, context):
    """Handler for the /hello command"""
    await update.message.reply_text("Hello there! This is a second command.")

def run_bot():
    """Run the Telegram bot in a background thread."""
    token = os.environ.get("TELEGRAM_TOKEN")
    application = Application.builder().token(token).build()
    
    # Add your two commands here
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hello", hello))
    
    # Start polling
    application.run_polling()

# --- FLASK WEB SERVER (To keep Render happy) ---
app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health():
    return "Bot is running", 200

# --- MAIN ENTRY POINT ---
if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start the Flask web server (Render requires listening on $PORT)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
