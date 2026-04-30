import requests
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# memory store
user_memory = {}

def get_memory(user_id, text):
    history = user_memory.get(user_id, [])
    history.append(text)
    if len(history) > 5:
        history.pop(0)
    user_memory[user_id] = history
    return " ".join(history)

# emoji system
def get_emoji(text):
    text = text.lower()
    if "sad" in text or "kharap" in text:
        return "😢"
    elif "happy" in text or "valo" in text:
        return "😄"
    elif "angry" in text or "rag" in text:
        return "😡"
    elif "love" in text:
        return "❤️"
    else:
        return "🙂"

# HuggingFace API
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def ai_reply(text):
    try:
        res = requests.post(API_URL, headers=headers, json={"inputs": text})
        data = res.json()

        if isinstance(data, list):
            return data[0].get("generated_text", "বুঝতে পারছি না")
        else:
            return "আবার বলো"
    except:
        return "Problem হচ্ছে"

# message handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    await context.bot.send_chat_action(chat_id=user_id, action="typing")
    await asyncio.sleep(1)

    context_text = get_memory(user_id, text)
    emoji = get_emoji(text)
    reply = ai_reply(context_text)

    await update.message.reply_text(emoji + " " + reply)

# Telegram bot token
TOKEN = os.getenv("8671489741:AAGtPB8KvA1JrDsHoWNEdfJHdlg-RbbAhds")

# app start
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("Bot running...")
app.run_polling()
