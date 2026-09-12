import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
RENDER_URL = "https://mygohbot.onrender.com"  # <-- Change this to YOUR actual Render URL

# --- BOT COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your simple bot.")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello there! This is a second command.")

# --- KEYWORD AUTO-REPLIES ---
KEYWORD_REPLIES = {
    "hello": "joon",
    "hi": "khastani hasti?",
    "bye": "siktir",
    "thanks": "fada",
    "thank you": "eshgh",
    "help": "goshadam nasakhtam.",
    "how are you": "Awli",
    "your name": "goh bot, zade ArianSA89",
    "good morning": "Good morning! ☀️",
    "good night": "shab o roegar khosh",
}

async def keyword_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check the message for keywords and reply with a preset message."""
    user_message = update.message.text.lower().strip()

    for keyword, reply in KEYWORD_REPLIES.items():
        if keyword in user_message:
            await update.message.reply_text(reply)
            return

    # Fallback if nothing matched
    await update.message.reply_text("I don't know that one yet! Try 'help'.")

# --- BUILD THE APPLICATION ---
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("hello", hello))
application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_reply)
)

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
    asyncio.run(setup_webhook())
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
