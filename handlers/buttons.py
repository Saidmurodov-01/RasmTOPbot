from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.messages import MESSAGES

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    lang = context.user_data.get("lang", "uz")
    msgs = MESSAGES.get(lang, MESSAGES['uz'])

    # 📞 Admin bilan bog‘lanish
    if data == "contact":
        context.user_data["awaiting_admin"] = True
        await query.message.edit_text(
            msgs["admin_prompt"],
            reply_markup=InlineKeyboardMarkup(msgs["menu"])
        )

    # ℹ️ Bot haqida
    elif data == "about":
        await query.message.edit_text(
            msgs["about_text"],   # ko‘p tilli matn
            reply_markup=InlineKeyboardMarkup(msgs["menu"])
        )

    # 🌐 Tilni o‘zgartirish
    elif data == "lang_select":
        current_lang = context.user_data.get("lang", "uz")
        next_lang = "ru" if current_lang == "uz" else "en" if current_lang == "ru" else "uz"
        context.user_data["lang"] = next_lang
        msgs = MESSAGES[next_lang]

        await query.message.edit_text(
            msgs["search_prompt"],
            reply_markup=InlineKeyboardMarkup(msgs["menu"])
        )

    # ❌ Noma'lum tugma
    else:
        await query.message.edit_text(
            "❌ Noma'lum tugma bosildi.",
            reply_markup=InlineKeyboardMarkup(msgs["menu"])
        )