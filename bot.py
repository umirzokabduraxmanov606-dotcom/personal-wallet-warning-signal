import os
from flask import Flask, request
import telebot

# The BOT_TOKEN will be stored as an environment variable on Render
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# --- Telegram webhook receiver ---
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


# --- Home route (for testing Render service) ---
@app.route("/", methods=["GET"])
def home():
    return "PWWS Telegram Bot is running ✔️", 200


# --- BOT LOGIC ---

@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = (
        "👋 Hello!\n"
        "Welcome to the *Personal Wallet Warning Signal (PWWS)* bot.\n\n"
        "PWWS helps detect potentially risky or scam crypto wallet addresses, "
        "making your transactions safer.\n\n"
        "Send me any Ethereum wallet address (starting with `0x`).\n"
        "For now, I will return a *demo* risk check."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: True)
def handle_wallet(message):
    addr = message.text.strip()

    # Simple demo validation
    if addr.startswith("0x") and len(addr) == 42:
        reply = (
            "🔍 *Demo Wallet Check*\n\n"
            f"Address: `{addr}`\n\n"
            "This is only a *test mode* response.\n"
            "In the next stage, the bot will connect to the PWWS backend "
            "and provide real scam/risk detection from live databases."
        )
        bot.send_message(message.chat.id, reply, parse_mode="Markdown")
    else:
        bot.reply_to(
            message,
            "Please send a valid Ethereum wallet address (must start with `0x` and be 42 characters long)."
        )


# Render will run this using Gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
