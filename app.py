import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
RENDER_URL = "https://mygohbot.onrender.com"  # Render sets this automatically

# --- BOT COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your simple bot.")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello there! This is a second command.")

# --- BUILD THE APPLICATION ---
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("hello", hello))

# --- FLASK WEB SERVER ---
app = Flask(__name__)

@app.route("/")
@app.route("/health")
def health():
    return "Bot is running", 200

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    """Handle incoming Telegram updates via webhook."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok", 200

# --- STARTUP: Set the webhook ---
async def setup_webhook():
    await application.initialize()
    await application.bot.set_webhook(f"{RENDER_URL}/webhook/{TOKEN}")
    print(f"Webhook set to {RENDER_URL}/webhook/{TOKEN}")

if __name__ == "__main__":
    # Set the webhook on startup
    asyncio.run(setup_webhook())
    # Run the Flask server (Render will hit our /webhook route)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
