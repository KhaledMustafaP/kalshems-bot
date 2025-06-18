import logging
from telegram import Bot, Poll
from telegram.ext import ApplicationBuilder
import schedule
import asyncio
import datetime

# 🔑 استبدل هذا بالتوكن الخاص فيك من BotFather
BOT_TOKEN = '7104783346:AAGtSznA02gw8eIq8Y1zbaHWsPLCjHPCoCY'
CHAT_ID = '@KalshemsKhatmahBot'  # مثال: @kalshams_channel

# 🔢 الحزب الحالي (يمكن تطويره لتخزين خارجي)
current_hizb = 1

async def send_hizb_message(app):
    global current_hizb
    text = f"📖 #ختمة_كالشمس\nورد اليوم: الحزب رقم {current_hizb}\n⏳ لا تنسوا تقرأوه اليوم!"
    await app.bot.send_message(chat_id=CHAT_ID, text=text)

async def send_poll(app):
    global current_hizb
    await app.bot.send_poll(
        chat_id=CHAT_ID,
        question=f"هل قرأت ورد اليوم؟ (الحزب {current_hizb})",
        options=["✅ نعم", "❌ لا"],
        is_anonymous=False,
        allows_multiple_answers=False
    )
    current_hizb += 1
    if current_hizb > 60:
        current_hizb = 1

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
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
