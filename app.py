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
    user = update.effective_user
    print(f"=== USER STARTED BOT ===")
    print(f"ID: {user.id}")
    print(f"Name: {user.first_name} {user.last_name or ''}")
    print(f"Username: @{user.username or 'none'}")
    print(f"========================")
    await update.message.reply_text("کیستی ای مارکو.")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلامd.")

# --- KEYWORD AUTO-REPLIES ---
KEYWORD_REPLIES = {
    "سلام": "علیک",
    " گوه بات": " دلم جون",
    "بای": "صیک",
    "مرسی": "فدا",
    "مرسی زیاد": "عشق",
    "کمک": "@ArianSa89.",
    "چطوری": "عالی",
    "اسمت": "گوه بات،زاده ارین",
    "صبح بخیر": "صبح بخیررررر",
    "شبخوش": "شبو روزگارت خوش",
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
