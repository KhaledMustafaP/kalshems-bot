import logging
from telegram import Bot, Poll
from telegram.ext import ApplicationBuilder
import schedule
import asyncio
import datetime
import nest_asyncio

# 🔑 استبدل هذا بالتوكن الخاص فيك من BotFather
BOT_TOKEN = '7104783346:AAGtSznA02gw8eIq8Y1zbaHWsPLCjHPCoCY'
CHAT_ID = 5523094937  # مثال: @kalshams_channel

# 📥 قراءة الحزب من ملف
def load_hizb():
    try:
        with open("hizb.txt", "r") as file:
            return int(file.read().strip())
    except:
        return 1

# 📤 كتابة الحزب في ملف
def save_hizb(hizb):
    with open("hizb.txt", "w") as file:
        file.write(str(hizb))

# 🔢 الحزب الحالي
current_hizb = load_hizb()

async def send_hizb_message(app):

    global current_hizb
    print(f"🔁 إرسال الحزب رقم {current_hizb} الآن...")  # للتجريب

    text = f"📖 #ختمة_كالشمس\nورد اليوم: الحزب رقم {current_hizb}\n⏳ لا تنسوا تقرأوه اليوم!"
    await app.bot.send_message(chat_id=CHAT_ID, text=text)

async def send_poll(app):
    global current_hizb
    await app.bot.send_poll(
        chat_id=CHAT_ID,
        question=f"هل قرأت ورد اليوم؟ (الحزب {current_hizb})",
        options=["✅ نعم", "❌ لا", "⏳ إن شاء الله بكرا"],
        is_anonymous=False,
        allows_multiple_answers=False
    )
    current_hizb += 1
    if current_hizb > 60:
        current_hizb = 1
    save_hizb(current_hizb)

async def scheduler(app):
    schedule.every().day.at("08:00").do(lambda: asyncio.create_task(send_hizb_message(app)))
    schedule.every().day.at("22:00").do(lambda: asyncio.create_task(send_poll(app)))
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    asyncio.create_task(scheduler(app))
    await app.run_polling()

if __name__ == '__main__':
    nest_asyncio.apply()
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
