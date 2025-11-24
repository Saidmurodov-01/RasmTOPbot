from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.messages import MESSAGES
from utils.logger import log_user

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update.message.from_user.id)

    lang = context.user_data.get("lang")
    if lang:
        msgs = MESSAGES.get(lang, MESSAGES['uz'])
        await update.message.reply_text(msgs['search_prompt'], reply_markup=InlineKeyboardMarkup(msgs['menu']))
        return

    langs = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data='lang_uz')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
    ])
    await update.message.reply_text("🌍 Choose your language:", reply_markup=langs)
