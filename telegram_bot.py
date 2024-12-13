import asyncio
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackContext
from time import sleep

# إعدادات البوت
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@YOUR_CHANNEL_ID"

# قائمة المنشورات
scheduled_posts = []

# إضافة منشور جديد
def add_post(update: Update, context: CallbackContext):
    global scheduled_posts
    if len(context.args) < 2:
        update.message.reply_text("يرجى إدخال المنشور والفاصل الزمني (بالثواني) بالشكل:\n/add_post [النص] [الفاصل الزمني]")
        return
    text = " ".join(context.args[:-1])
    delay = int(context.args[-1])
    scheduled_posts.append((text, delay))
    update.message.reply_text(f"تمت إضافة المنشور:\n{text}\nوسيُنشر بعد {delay} ثانية.")

# بدء النشر التلقائي
async def start_scheduled_posts(update: Update, context: CallbackContext):
    global scheduled_posts
    if not scheduled_posts:
        update.message.reply_text("لا توجد منشورات مجدولة.")
        return
    bot = Bot(token=BOT_TOKEN)
    for post, delay in scheduled_posts:
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=post)
            update.message.reply_text(f"تم نشر المنشور:\n{post}")
        except Exception as e:
            update.message.reply_text(f"خطأ أثناء النشر: {e}")
        await asyncio.sleep(delay)
    scheduled_posts = []
    update.message.reply_text("تم نشر جميع المنشورات بنجاح!")

# إعداد الأوامر
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("add_post", add_post))
dispatcher.add_handler(CommandHandler("start_posts", start_scheduled_posts))

# بدء البوت
updater.start_polling()
print("البوت يعمل الآن.")
updater.idle()