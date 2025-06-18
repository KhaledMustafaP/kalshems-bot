import logging
import asyncio
import nest_asyncio
import schedule
from datetime import datetime
from telegram import Bot
from telegram.ext import Application, CommandHandler

# 🔑 استبدل هذا بالتوكن الخاص فيك من BotFather
BOT_TOKEN = '7104783346:AAGtSznA02gw8eIq8Y1zbaHWsPLCjHPCoCY'
CHAT_ID = 5523094937  # مثال: @kalshams_channel

# تفعيل nest_asyncio
nest_asyncio.apply()

# إعداد اللوج
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# إنشاء التطبيق
app = Application.builder().token(TOKEN).build()

# دالة إرسال الحزب اليومي
async def send_daily_ward():
    # حساب رقم الحزب بناءً على اليوم في الشهر
    today = datetime.now()
    hizb_number = (today.day % 60) + 1
    message = f"📖 ورد اليوم من القرآن الكريم:\nالحزب رقم {hizb_number}\nلا تنس قراءة وردك اليومي ✨"

    await app.bot.send_message(chat_id=CHANNEL_ID, text=message)

# دالة إرسال الاستطلاع في نهاية اليوم
async def send_poll():
    await app.bot.send_poll(
        chat_id=CHANNEL_ID,
        question="📊 هل قرأت وردك القرآني اليوم؟",
        options=["✅ نعم قرأت", "❌ لا للأسف"],
        is_anonymous=False
    )

# مهمة الجدولة اليومية
def schedule_tasks():
    schedule.every().day.at("08:00").do(lambda: asyncio.create_task(send_daily_ward()))
    schedule.every().day.at("20:00").do(lambda: asyncio.create_task(send_poll()))

# حلقة تشغيل الجدولة
async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

# دالة البدء
async def start(update, context):
    await update.message.reply_text("أهلاً بك! هذا بوت ورد كالشمس 🌞📖")

app.add_handler(CommandHandler("start", start))

# التشغيل
async def main():
    schedule_tasks()
    asyncio.create_task(scheduler_loop())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())