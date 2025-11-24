import os
from dotenv import load_dotenv
from telegram import InputMediaPhoto, InlineKeyboardMarkup
from data.messages import MESSAGES
from utils.logger import log_user
from utils.translator import translate_to_english
from utils.pexels import search_pexels

load_dotenv()
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

async def handle_text(update, context):
    log_user(update.message.from_user.id)
    text = update.message.text
    lang = context.user_data.get("lang", "uz")
    msgs = MESSAGES.get(lang, MESSAGES['uz'])

    # Admin rejimi
    if context.user_data.get("awaiting_admin"):
        if ADMIN_CHAT_ID:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"📩 Yangi xabar:\n\n{text}\n\n👤 User ID: {update.message.from_user.id}"
            )
            await update.message.reply_text(msgs['admin_sent'])
        else:
            await update.message.reply_text("❌ Admin ID sozlanmagan.")
        context.user_data["awaiting_admin"] = False
        return

    # Qidiruv
    query = translate_to_english(text)
    urls = search_pexels(query, per_page=10)

    if urls:
        # 6 ta rasmni albom sifatida yuboramiz
        media = []
        for i, url in enumerate(urls[:10]):
            if i == 0:
                media.append(InputMediaPhoto(media=url, caption=f"🔎 {text}"))
            else:
                media.append(InputMediaPhoto(media=url))

        await update.message.reply_media_group(media)

        # Istasak, tugmalarni alohida xabar bilan qayta ko‘rsatamiz
        await update.message.reply_text(
            msgs['search_prompt'],
            reply_markup=InlineKeyboardMarkup(msgs['menu'])
        )
    else:
        await update.message.reply_text(msgs['not_found'])