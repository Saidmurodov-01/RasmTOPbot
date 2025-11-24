from telegram import InlineKeyboardButton

MESSAGES = {
    "uz": {
        "search_prompt": "🔍 Qidiruv uchun so‘z yuboring:",
        "menu": [
            [InlineKeyboardButton("📞 Admin bilan bog‘lanish", callback_data="contact")],
            [InlineKeyboardButton("ℹ️ Bot haqida", callback_data="about")],
            [InlineKeyboardButton("🌐 Tilni o‘zgartirish", callback_data="lang_select")],
        ],
        "admin_prompt": "✍️ Admin uchun xabar yozing:",
        "admin_sent": "✅ Xabaringiz adminga yuborildi.",
        "not_found": "❌ Rasm topilmadi.",
        "about_text": "ℹ️ Bu bot Pexels API orqali rasm qidiradi va foydalanuvchiga yuboradi.",
        "categories_map": {}
    },
    "ru": {
        "search_prompt": "🔍 Отправьте слово для поиска:",
        "menu": [
            [InlineKeyboardButton("📞 Связаться с админом", callback_data="contact")],
            [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
            [InlineKeyboardButton("🌐 Сменить язык", callback_data="lang_select")],
        ],
        "admin_prompt": "✍️ Напишите сообщение для админа:",
        "admin_sent": "✅ Ваше сообщение отправлено администратору.",
        "not_found": "❌ Изображения не найдены.",
        "about_text": "ℹ️ Этот бот ищет изображения через Pexels API и отправляет их пользователю.",
        "categories_map": {}
    },
    "en": {
        "search_prompt": "🔍 Send a word to search:",
        "menu": [
            [InlineKeyboardButton("📞 Contact admin", callback_data="contact")],
            [InlineKeyboardButton("ℹ️ About the bot", callback_data="about")],
            [InlineKeyboardButton("🌐 Change language", callback_data="lang_select")],
        ],
        "admin_prompt": "✍️ Write a message to the admin:",
        "admin_sent": "✅ Your message has been sent to the admin.",
        "not_found": "❌ No images found.",
        "about_text": "ℹ️ This bot searches images using the Pexels API and sends them to the user.",
        "categories_map": {}
    }
}