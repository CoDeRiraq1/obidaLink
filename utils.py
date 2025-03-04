from telegram import Update
from config import CHANNEL_USERNAME, ADMIN_ID
from database import Database

db = Database()

async def is_member(update: Update, user_id: int) -> bool:
    """التحقق من اشتراك المستخدم في القناة"""
    try:
        chat_member = await update.effective_chat.get_member(user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطأ في التحقق: {e}")
        return False

def generate_referral_link(user_id: int, bot_username: str) -> str:
    """توليد رابط الإحالة"""
    return f"https://t.me/{bot_username}?start={user_id}"
