import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# إعداد تسجيل الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ============ الإعدادات ============
# ملاحظة: التوكن سيتم وضعه في إعدادات Render لاحقاً (كإجراء أمني)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "9058598200:AAELVfnslLRcIU-yZKJckEimJOVnvb5jYM0")

# https://www.instagram.com/aldar_770
INSTAGRAM_URL = "https://www.instagram.com/aldar_770" 

# ============ البيانات ============
SUBJECTS = {
    "رياضيات": {
        "ملف الشرح": {"type": "file", "url": "https://example.com/math.pdf"},
        "تمارين": {"type": "file", "url": "https://example.com/exercises.pdf"},
    },
    "فيزياء": {
        "ملف الشرح": {"type": "file", "url": "https://example.com/physics.pdf"},
        "تمارين": {"type": "file", "url": "https://example.com/exercises.pdf"},
    },
    "إنستقرام": {
        "زيارة حسابي": {"type": "instagram"},
    },
}

# ============ دوال مساعدة ============
def build_main_menu() -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    for subject in SUBJECTS:
        row.append(InlineKeyboardButton(subject, callback_data=f"subj:{subject}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def build_subject_menu(subject: str) -> InlineKeyboardMarkup:
    keyboard = []
    for option_name, option_data in SUBJECTS[subject].items():
        if option_data["type"] == "instagram":
            keyboard.append([InlineKeyboardButton(f"📸 {option_name}", url=INSTAGRAM_URL)])
        else:
            keyboard.append([InlineKeyboardButton(f"📄 {option_name}", callback_data=f"opt:{subject}:{option_name}")])
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back:main")])
    return InlineKeyboardMarkup(keyboard)

# ============ معالجات الأوامر ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك!\nاختر المادة التي تريدها:",
        reply_markup=build_main_menu()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.edit_message_text("👋 اختر المادة التي تريدها:", reply_markup=build_main_menu())
        return

    if data.startswith("subj:"):
        subject = data.split(":", 1)[1]
        await query.edit_message_text(
            f"📚 *{subject}*\nاختر أحد الخيارات:",
            reply_markup=build_subject_menu(subject),
            parse_mode="Markdown"
        )
        return

    if data.startswith("opt:"):
        _, subject, option_name = data.split(":", 2)
        option_data = SUBJECTS[subject][option_name]
        if option_data["type"] == "file":
            await query.edit_message_text(
                f"📥 *{option_name}*\n\n[اضغط هنا لتحميل الملف]({option_data['url']})",
                parse_mode="Markdown"
            )
        
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=f"subj:{subject}")]])
        )
        return

# ============ تشغيل البوت ============
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("✅ البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
