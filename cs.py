import os
from pyrogram import Client, filters
from dotenv import load_dotenv

# تحميل المتغيرات من ملف البيئة
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# إنشاء عميل البوت
app = Client(
    "telegram_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# فلتر لالتقاط الأمر والرد على الرسائل
@app.on_message(filters.command("تحميل", prefixes=".") & filters.reply)
async def download_and_save(_, message):
    # التأكد من وجود رد على الرسالة
    if not message.reply_to_message:
        await message.reply("❌ يجب الرد على رابط تيليجرام لتنزيله!")
        return

    # الحصول على الرابط من الرسالة
    reply_message = message.reply_to_message
    if not reply_message.text:
        await message.reply("❌ لا توجد رسالة نصية تحتوي على رابط!")
        return

    link = reply_message.text.strip()
    
    # محاولة تنزيل الملف
    try:
        sent_message = await message.reply("⏳ جاري تنزيل المحتوى...")
        downloaded_file = await app.download_media(link)
        await sent_message.edit("✅ تم التنزيل بنجاح! ⏳ جاري الإرسال إلى الرسائل المحفوظة...")

        # إرسال الملف إلى الرسائل المحفوظة
        await app.send_document("me", downloaded_file, caption="📥 تم التنزيل من الرابط:\n" + link)
        await sent_message.edit("✅ تم الإرسال إلى الرسائل المحفوظة بنجاح!")
        
        # حذف الملف من الجهاز
        os.remove(downloaded_file)

    except Exception as e:
        await message.reply(f"❌ حدث خطأ أثناء التنزيل: {e}")

# بدء تشغيل البوت
if __name__ == "__main__":
    app.run()
