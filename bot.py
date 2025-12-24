from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import os
import json

TOKEN = os.environ["8555310397:AAFo28I_yZ6HMoNxAg8cR3sCfbmVg42W-D4"]
DATA_FILE = "data.json"

# ---------- storage ----------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

# ---------- commands ----------

async def start(update: Update, context):
    kb = [[InlineKeyboardButton("TV Shows", callback_data="tv")]]
    await update.message.reply_text("Choose:", reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update: Update, context):
    q = update.callback_query
    await q.answer()

    if q.data == "tv":
        kb = [[InlineKeyboardButton("Silo", callback_data="silo")]]
        await q.edit_message_text("TV Shows:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data == "silo":
        kb = [[InlineKeyboardButton("Season 1", callback_data="silo_s1")]]
        await q.edit_message_text("Silo:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data == "silo_s1":
        eps = data.get("silo", {}).get("s1", [])
        if not eps:
            await q.edit_message_text("No episodes saved.")
            return

        await q.edit_message_text("Sending Silo Season 1...")
        for file_id in eps:
            await context.bot.send_video(
                chat_id=q.message.chat_id,
                video=file_id
            )

# ---------- save forwarded episodes ----------

async def save_episode(update: Update, context):
    msg = update.message

    if not msg.video:
        return

    file_id = msg.video.file_id
    caption = (msg.caption or "").lower()

    # VERY SIMPLE parser
    if "silo" in caption and "s1" in caption:
        data.setdefault("silo", {}).setdefault("s1", []).append(file_id)
        save_data(data)
        await msg.reply_text("Saved: Silo Season 1 episode")

# ---------- run ----------

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.VIDEO & filters.FORWARDED, save_episode))

app.run_polling()
