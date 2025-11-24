import json
from config import ADMIN_CHAT_ID

async def stat(update, context):
    if update.message.from_user.id != ADMIN_CHAT_ID:
        return
    try:
        with open("data/user_log.json", "r") as f:
            users = json.load(f)
        count = len(users)
    except:
        count = 0
    await update.message.reply_text(f"👥 Botdan foydalanganlar soni: {count} ta")
