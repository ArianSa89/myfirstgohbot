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

TOKEN = os.environ.get("TELEGRAM_TOKEN")
RENDER_URL = "https://mygohbot.onrender.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    print("=== USER STARTED BOT ===")
    print(f"ID: {user.id}")
    print(f"Name: {user.first_name} {user.last_name or ''}")
    print(f"Username: @{user.username or 'none'}")
    print("========================")

    await update.message.reply_text("کیستی ای مارکو.")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلامd.")


KEYWORD_REPLIES = {
    "سلام": "علیک",
    "گوه بات": "دلم جون",
   " " فعلا عشق"" خدافظ",
    "مرسی": "فدا",
    "مرسی زیاد": "عشق",
    "کمک": "@ArianSa89.",
    "چطوری": "عالی",
    "اسمت": "گوه بات، زاده ارین",
    "صبح بخیر": "صبح بخیررررر",
    "شبخوش": "شبو روزگارت خوش",
}


async def keyword_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message or not message.text:
        return

    user_message = message.text.lower().strip()
    chat_type = message.chat.type  # "private", "group", or "supergroup"

    # Is this a private chat?
    is_private = chat_type == "private"

    # Is this a reply to one of the bot's messages?
    is_reply_to_bot = False
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        if replied_user and replied_user.id == context.bot.id:
            is_reply_to_bot = True

    # Is the bot mentioned in the message?
    is_mentioned = False
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                username = message.text[
                    entity.offset:entity.offset + entity.length
                ]
                if username.lower() == f"@{context.bot.username.lower()}":
                    is_mentioned = True
                    break

    # Only respond if private, mentioned, or replied to
    should_respond = is_private or is_mentioned or is_reply_to_bot

    if not should_respond:
        return

    # Look for a matching keyword reply
    matched_reply = None
    for keyword, reply in KEYWORD_REPLIES.items():
        if keyword in user_message:
            matched_reply = reply
            break

    if matched_reply:
        await message.reply_text(matched_reply)
        return

    # Fallback if the bot was addressed but no keyword matched
    await message.reply_text("کیستی ای مارکو.")


application = Application.builder().token(TOKEN).build()

application.add_handler(
    CommandHandler("start", start)
)

application.add_handler(
    CommandHandler("hello", hello)
)

application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        keyword_reply
    )
)


app = Flask(__name__)


@app.route("/")
@app.route("/health")
def health():
    return "Bot is running", 200


@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(
        request.get_json(force=True),
        application.bot
    )

    asyncio.run(
        application.process_update(update)
    )

    return "ok", 200


async def setup_webhook():
    await application.initialize()

    await application.bot.set_webhook(
        f"{RENDER_URL}/webhook/{TOKEN}"
    )

    print(
        f"Webhook set to "
        f"{RENDER_URL}/webhook/{TOKEN}"
    )


if __name__ == "__main__":
    asyncio.run(setup_webhook())

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
