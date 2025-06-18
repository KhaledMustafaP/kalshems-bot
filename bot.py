import logging
import asyncio
import nest_asyncio
import schedule
from datetime import datetime
from telegram import Bot
from telegram.ext import Application, CommandHandler
from flask import Flask
import threading

# 🔑 استبدل هذا بالتوكن الخاص فيك من BotFather
BOT_TOKEN = '7104783346:AAGtSznA02gw8eIq8Y1zbaHWsPLCjHPCoCY'
CHAT_ID = 5523094937  # ID القناة أو الشخص

# ===== إعدادات اللوج =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ===== تفعيل nest_asyncio لحل مشكلة event loop =====
nest_asyncio.apply()

# ===== إنشاء تطبيق التليجرام =====
app = Application.builder().token(BOT_TOKEN).build()

# ===== دوال البوت =====
async def send_daily_ward():
    today = datetime.now()
    hizb_number = (today.day % 60) + 1
    message = f"📖 ورد اليوم من القرآن الكريم:\nالحزب رقم {hizb_number}\nلا تنس قراءة وردك اليومي ✨"
    await app.bot.send_message(chat_id=CHANNEL_ID, text=message)

async def send_poll():
    await app.bot.send_poll(
        chat_id=CHANNEL_ID,
        question="📊 هل قرأت وردك القرآني اليوم؟",
        options=["✅ نعم قرأت", "❌ لا للأسف"],
        is_anonymous=False
    )

async def start(update, context):
    await update.message.reply_text("أهلاً بك! هذا بوت ورد كالشمس 🌞📖")

app.add_handler(CommandHandler("start", start))

# ===== جدولة المهام =====
def schedule_tasks():
    schedule.every().day.at("08:00").do(lambda: asyncio.create_task(send_daily_ward()))
    schedule.every().day.at("20:00").do(lambda: asyncio.create_task(send_poll()))

async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

# ===== Web Server باستخدام Flask =====
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running OK"

def run_web():
    flask_app.run(host="0.0.0.0", port=10000)

# ===== تشغيل كل إشي =====
async def main():
    schedule_tasks()
    asyncio.create_task(scheduler_loop())
    threading.Thread(target=run_web).start()  # تشغيل السيرفر على ثريد منفصل
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
