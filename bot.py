import json, random, re, requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = "8154843224:AAFC9kfq1KBba6xbjPHBiv7juNNSUAEbsRA"
PEXELS_API_KEY = "KuBQx07WZQa4me3SNUGRERQ1tq3rRlLdAQXkFxK7RGRw3kfasWqqztNa"
ADMIN_CHAT_ID = 7340274152

def log_user(user_id):
    try:
        with open("user_log.json", "r") as f:
            users = json.load(f)
    except:
        users = []
    if user_id not in users:
        users.append(user_id)
        with open("user_log.json", "w") as f:
            json.dump(users, f)

def search_pexels(query):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": query, "per_page": 20}
        r = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
        data = r.json()
        photos = data.get("photos", [])
        urls = [p["src"]["medium"] for p in photos]
        return random.sample(urls, k=min(10, len(urls)))
    except:
        return []

MESSAGES = {
    'uz': {
        'start': "🌍 Tilni tanlang:",
        'menu': [
            [InlineKeyboardButton("📞 Adminga murojat", callback_data='contact')],
            [InlineKeyboardButton("ℹ️ Bot haqida", callback_data='about')],
            [InlineKeyboardButton("🌐 Tilni o‘zgartirish", callback_data='lang_select')]
        ],
        'categories': [
            [InlineKeyboardButton("🌳 Tabiat", callback_data='cat_nature'),
             InlineKeyboardButton("🚗 Mashinalar", callback_data='cat_cars')],
            [InlineKeyboardButton("🐾 Hayvonlar", callback_data='cat_animals'),
             InlineKeyboardButton("🏙 Shahar", callback_data='cat_city')]
        ],
        'categories_map': {
            'nature': 'nature',
            'cars': 'cars',
            'animals': 'animals',
            'city': 'city landscape'
        },
        'search_prompt': "🗂 Matnni ingliz tilida kiriting yoki kategoriya tanlang:",
        'admin_prompt': "✏️ Savol yoki taklif yozing:",
        'admin_sent': "✅ Xabaringiz adminga yuborildi.",
        'not_found': "😕 Rasm topilmadi."
    },
    'ru': {
        'start': "🌍 Выберите язык:",
        'menu': [
            [InlineKeyboardButton("📞 Связаться с админом", callback_data='contact')],
            [InlineKeyboardButton("ℹ️ О боте", callback_data='about')],
            [InlineKeyboardButton("🌐 Сменить язык", callback_data='lang_select')]
        ],
        'categories': [
            [InlineKeyboardButton("🌳 Природа", callback_data='cat_nature'),
             InlineKeyboardButton("🚗 Машины", callback_data='cat_cars')],
            [InlineKeyboardButton("🐾 Животные", callback_data='cat_animals'),
             InlineKeyboardButton("🏙 Город", callback_data='cat_city')]
        ],
        'categories_map': {
            'nature': 'nature',
            'cars': 'cars',
            'animals': 'animals',
            'city': 'city landscape'
        },
        'search_prompt': "🗂 Введите запрос на английском или выберите категорию:",
        'admin_prompt': "✏️ Напишите ваш вопрос или проблему:",
        'admin_sent': "✅ Сообщение отправлено администратору.",
        'not_found': "😕 Изображения не найдены."
    },
    'en': {
        'start': "🌍 Choose your language:",
        'menu': [
            [InlineKeyboardButton("📞 Contact admin", callback_data='contact')],
            [InlineKeyboardButton("ℹ️ About bot", callback_data='about')],
            [InlineKeyboardButton("🌐 Change language", callback_data='lang_select')]
        ],
        'categories': [
            [InlineKeyboardButton("🌳 Nature", callback_data='cat_nature'),
             InlineKeyboardButton("🚗 Cars", callback_data='cat_cars')],
            [InlineKeyboardButton("🐾 Animals", callback_data='cat_animals'),
             InlineKeyboardButton("🏙 City", callback_data='cat_city')]
        ],
        'categories_map': {
            'nature': 'nature',
            'cars': 'cars',
            'animals': 'animals',
            'city': 'city landscape'
        },
        'search_prompt': "🗂 Type in English or choose a category:",
        'admin_prompt': "✏️ Type your question or issue:",
        'admin_sent': "✅ Your message has been sent to the admin.",
        'not_found': "😕 No images found."
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update.message.from_user.id)
    langs = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data='lang_uz')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
    ])
    await update.message.reply_text("🌍 Choose your language:", reply_markup=langs)
    context.user_data.clear()

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    lang = context.user_data.get("lang", "uz")
    msgs = MESSAGES.get(lang, MESSAGES['uz'])

    if data.startswith("lang_"):
        context.user_data["lang"] = data.replace("lang_", "")
        msgs = MESSAGES.get(context.user_data["lang"], MESSAGES['uz'])

        if q.message.text != msgs['search_prompt']:
            try:
                await q.message.edit_text(msgs['search_prompt'], reply_markup=InlineKeyboardMarkup(msgs['menu']))
            except:
                pass
        return

    if data == "contact":
        context.user_data["awaiting_admin"] = True
        await q.message.edit_text(msgs['admin_prompt'])
    elif data == "about":
        await q.message.edit_text("📦 RasmTop — Pexels API orqali rasm izlaydi.")
    elif data == "lang_select":
        await start(update, context)
    elif data.startswith("cat_"):
        query = msgs['categories_map'].get(data.replace("cat_", ""), "nature")
        urls = search_pexels(query)
        if urls:
            for url in urls:
                await q.message.reply_photo(photo=url)
        else:
            await q.message.reply_text(msgs['not_found'])

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update.message.from_user.id)
    text = update.message.text
    lang = context.user_data.get("lang", "uz")
    msgs = MESSAGES.get(lang, MESSAGES['uz'])

    if context.user_data.get("awaiting_admin"):
        context.user_data["awaiting_admin"] = False
        user = update.message.from_user
        username = f"@{user.username}" if user.username else "No username"
        msg = f"📨 Xabar:\n👤 {user.full_name} ({username})\n📝 {text}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)
        await update.message.reply_text(msgs['admin_sent'])
        return

    if not re.match(r'^[a-zA-Z\s\-]+$', text.strip()):
        await update.message.reply_text("❗ Faqat inglizcha so‘z yuboring.")
        return

    urls = search_pexels(text)
    if urls:
        for url in urls:
            await update.message.reply_photo(photo=url, caption=f"🔎 {text}")
    else:
        await update.message.reply_text(msgs['not_found'])

async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_CHAT_ID:
        return
    try:
        with open("user_log.json", "r") as f:
            users = json.load(f)
        count = len(users)
    except:
        count = 0
    await update.message.reply_text(f"👥 Botdan foydalanganlar soni: {count} ta")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stat", stat))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Bot ish tushdi! (Statistikali, 3 tilda)")

    app.run_polling()
