import logging
import asyncio
from telegram import Bot
import nest_asyncio
import schedule
from datetime import datetime
from telegram.ext import Application, CommandHandler
from flask import Flask
import threading

# ===== إعدادات أساسية =====
BOT_TOKEN = '7104783346:AAGtSznA02gw8eIq8Y1zbaHWsPLCjHPCoCY'
CHAT_ID = '@shamsju'

# ===== اللوج =====
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

nest_asyncio.apply()
app = Application.builder().token(BOT_TOKEN).build()

# ===== التعامل مع ملف الجزء =====
def read_juz():
    try:
        with open("progress.txt", "r") as file:
            return int(file.read().strip())
    except:
        return 1

def write_juz(juz):
    with open("progress.txt", "w") as file:
        file.write(str(juz))

# ===== المهام اليومية =====
async def send_daily_ward():
    juz_number = read_juz()
    message = f"📖 الورد اليومي: الجزء ({juz_number})\nلا تنسى قراءة وردك لليوم ✨💙"
    await app.bot.send_message(chat_id=CHAT_ID, text=message)

    next_juz = juz_number + 1 if juz_number < 30 else 1
    write_juz(next_juz)



# ===== الأوامر =====
async def start(update, context):
    await update.message.reply_text("أهلاً بك! هذا بوت ورد كالشمس 🌞📖")

async def reset(update, context):
    write_juz(1)
    await update.message.reply_text("✅ تم إعادة العداد إلى الجزء 1")

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reset", reset))

# ===== الجدولة =====
def schedule_tasks():
    schedule.every().day.at("06:00").do(lambda: asyncio.create_task(send_daily_ward()))  # 8 صباحاً بتوقيت الأردن

async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

# ===== Web Server ليدعمه UptimeRobot أو Ping =====
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running OK"

def run_web():
    flask_app.run(host="0.0.0.0", port=10000)

# ===== التشغيل =====
async def main():
    bot = Bot(token=BOT_TOKEN)

    await bot.send_message(chat_id=CHAT_ID, text="🌞 هذا اختبار إرسال من البوت للقناة!")
    schedule_tasks()
    asyncio.create_task(scheduler_loop())
    threading.Thread(target=run_web).start()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
