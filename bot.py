import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- ✅ TOKEN CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "7010932994:AAFoIqUi6mhosfuFFarrANZmfRffOuz_fdI"
TOGATHER_API_KEY = "6b9170474f79ca06987a8ad12a39c5aeecab90c62ea68eb93f7c60419e0b48fe"

# --- 🧠 AI Answer from Together API ---
def get_answer_from_together(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGATHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.9
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        result = response.json()
        return result["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- 🌐 Translate to Hindi ---
def translate_to_hindi(text):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": "en|hi"}
    try:
        res = requests.get(url, params=params)
        return res.json()['responseData']['translatedText']
    except:
        return "हिंदी अनुवाद उपलब्ध नहीं है।"

# --- ✅ /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Ask me any Class 12 question in English or Hindi.\nI’ll reply in both languages (English + हिंदी).")

# --- ✉️ Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text.strip()
    await update.message.reply_text("🧠 Thinking... please wait...")

    english_ans = get_answer_from_together(question)
    hindi_ans = translate_to_hindi(english_ans)

    final_reply = f"""❓ *Question:* {question}

🇬🇧 *English:*
{english_ans}

🇮🇳 *हिंदी:*
{hindi_ans}
"""
    await update.message.reply_text(final_reply, parse_mode="Markdown")

# --- 🚀 Bot Starter ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()