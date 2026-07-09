import os
import sqlite3
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_URL = "https://t.me/ekaterinbursha"
GUIDE_PATH = "guide.pdf"
ADMIN_ID = 343721610

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()

def save_user(user_id):
    conn = sqlite3.connect("users.db")
    conn.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    rows = conn.execute("SELECT id FROM users").fetchall()
    conn.close()
    return [r[0] for r in rows]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    keyboard = [[InlineKeyboardButton("📥 Получить гайд", callback_data="get_guide")]]
    await update.message.reply_text(
        "Я живу в ЕКБ и несколько месяцев собирала этот гайд — кафе, архитектура, нишевые магазины и места куда хочется возвращаться. Дарю 🎁",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "get_guide":
        keyboard = [[InlineKeyboardButton("📲 Подписаться на канал", url=CHANNEL_URL)]]
        with open(GUIDE_PATH, "rb") as f:
            await query.message.reply_document(
                document=f,
                filename="Гайд по ЕКБ.pdf",
                caption="Держи гайд! 🗺️\n\nКаждый день про ЕКБ — в моём канале. Там ещё больше мест, историй и инсайдов 👇",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

async def
