import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardMarkup

# Import handlerlar
from handlers.buttons import handle_buttons
from handlers.text import handle_text
from data.messages import MESSAGES

# .env fayldan tokenni yuklaymiz
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start komandasi
async def start(update, context):
    lang = context.user_data.get("lang", "uz")
    msgs = MESSAGES.get(lang, MESSAGES['uz'])
    # Inline tugmalarni chiqaramiz
    await update.message.reply_text(
        msgs['search_prompt'],
        reply_markup=InlineKeyboardMarkup(msgs['menu'])
    )

def main():
    # Botni yaratamiz
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlerlarni qo‘shamiz
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_buttons))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Botni ishga tushiramiz
    print("🤖 Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    main()