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

# ===== الرسالة اليومية =====
async def send_daily_ward():
    message = "🌸 وردك اليومي: لا تنسَ أن تتلو آياتك اليوم بقلبٍ خاشع 💫"
    await app.bot.send_message(chat_id=CHAT_ID, text=message)

# ===== الأوامر =====
async def start(update, context):
    await update.message.reply_text("أهلاً بك! هذا بوت ورد كالشمس 🌞📖")

app.add_handler(CommandHandler("start", start))

# ===== الجدولة =====
def schedule_tasks():
    schedule.every().day.at("06:00").do(lambda: asyncio.create_task(send_daily_ward()))  # 6 صباحاً بتوقيت السيرفر

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
